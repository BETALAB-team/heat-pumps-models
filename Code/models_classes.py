import copy

import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error, root_mean_squared_error,r2_score
from scipy.optimize import minimize

class model_hp():
    
    allowed_plf_methods = [
            "direct_linear",
            "direct_quadratic",
            "ISO 13612-2 mod A",
            "ISO 13612-2 mod B",
            "C method"
            ]
    
    def __init__(self, plf_method = "direct_linear"):
        if plf_method not in self.allowed_plf_methods:
            raise TypeError(f"plf_method must be chosen from the following list: {self.allowed_plf_methods}")
            
        self.plf_method = plf_method
        
    def set_curve_df(self,curve):
        self.curve = copy.deepcopy(curve)
        
    def train_linear_model(self,df):       
        self.df = df
        
        "Divide between part load and full load operative points"
        df_FL = df[df['PLF']==1]
        df_PL = df[df['PLF']!=1]
        
        self.df_FL = df_FL
        self.df_PL = df_PL
        
        self.PLF, self.COP, self.X = self.get_inputs_function(self.df)
        self.PLF_PL, self.COP_PL, self.X_PL = self.get_inputs_function(self.df_PL)
        self.PLF_FL, self.COP_FL, self.X_FL = self.get_inputs_function(self.df_FL)
      
        "Create matrix and full load calculations"
        self.model_reg_FL = linear_model.LinearRegression().fit(self.X_FL, self.COP_FL)
        
        "Create matrix and part load calculations"
        COP_FL_pred = self.model_reg_FL.predict(self.X_PL)

        f_COP_model_FL = self.COP_PL/COP_FL_pred
        
        "Create matrix and calculations"
        if self.plf_method == "direct_linear":
            X_dir_lin = np.column_stack([self.X,self.PLF])
            self.model_reg = linear_model.LinearRegression().fit(X_dir_lin, self.COP)
            
        elif self.plf_method == "direct_quadratic":
            X_dir_qua = np.column_stack([self.X,self.PLF,self.PLF**2])   
            self.model_reg = linear_model.LinearRegression().fit(X_dir_qua, self.COP)
        else:
            self.calculate_f_cop(f_COP_model_FL)
            
    def train_exp_model(self,df):
        self.df = df
        self.df_FL = df[df['PLF']==1]
        self.df_PL = df[df['PLF']!=1]
        
        self.PLF, self.X, self.COP, self.A0 = self.get_inputs(self.df)
        self.PLF_PL, self.X_PL, self.COP_PL, self.A0_PL = self.get_inputs(self.df_PL)
        self.PLF_FL, self.X_FL, self.COP_FL, self.A0_FL = self.get_inputs(self.df_FL)
                      
        def fun(x0,xdata,ydata):
            fun_m = {
                    "direct_linear":self.f_method_d01,
                    "direct_quadratic":self.f_method_d02,
                    "ISO 13612-2 mod A":self.f_method_n,
                    "ISO 13612-2 mod B":self.f_method_n,
                    "C method":self.f_method_n,
                }[self.plf_method]
            Y_pred = fun_m(x0,xdata)
            return sum((Y_pred-ydata)**2)
        
        if self.plf_method in ["direct_linear","direct_quadratic"]:
            self.model_reg = minimize(fun, self.A0, args = (self.X, self.COP), method = 'L-BFGS-B')   
        else:
            self.model_reg = minimize(fun, self.A0, args = (self.X_FL, self.COP_FL), method = 'L-BFGS-B')
            A = self.model_reg['x']
            COP_FL_pred = A[0]*np.exp(A[1]*self.X_PL[:,0] + A[2]*self.X_PL[:,1]) + A[3]*self.X_PL[:,0]/self.X_PL[:,1] + A[4]    
            f_COP_model_FL = self.COP_PL/COP_FL_pred
            self.calculate_f_cop(f_COP_model_FL)
        
    def train_COP_model(self, df, Source_T = 7, Load_T = 35, COP = None):
        self.df = df
        self.df_FL = df[df['PLF']==1]
        self.df_PL = df[df['PLF']!=1]
        
        self.PLF_PL = np.array(self.df_PL["PLF"])
        
        COP_carnot = (Load_T + 273.15 )/ (Load_T - Source_T)
        
        if hasattr(self, "curve"):
            curve = copy.deepcopy(self.curve)
            curve = curve.set_index(curve['SET'])  
            COP = curve.loc[Source_T, 'COP_fl'] 
            self.eta_design = COP / COP_carnot # second principle efficency for full load data point
        else:
            if COP == None:
                raise ValueError("If no design points curve df has been set, COP at design load must be provided")
            self.eta_design = COP / COP_carnot     
        
        SET_PL = np.array(self.df_PL["SET [°C]"])
        LExT_PL = np.array(self.df_PL["LExT [°C]"])
        COP_PL = np.array(self.df_PL["COP"])
                
        COP_pred_PL = self.calc_COP_FL(LExT_PL, SET_PL)
        
        f_COP_model_FL = COP_PL/COP_pred_PL
        
        self.calculate_f_cop(f_COP_model_FL)
        
    def calculate_f_cop(self, f_COP_model_FL):
        if self.plf_method == "ISO 13612-2 mod A":
            
            "Method 1: f_cop by linear regression"
            def f_COP_fun(x):
                if not isinstance(x,np.ndarray):
                    x = np.array([x])
                f_COP=np.ones(len(x))
                for i in range(len(x)):
                    if  x[i] >= 0.25:
                        f_COP[i]=1;
                    else:
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)
                return f_COP
                    
            self.f_COP = lambda x : f_COP_fun(x)
            
                
        elif self.plf_method == "ISO 13612-2 mod B":
            if not hasattr(self, 'curve'):
                raise AttributeError("If model ISO 13612-2 mod B is choosen then a curve df needs to be provided by the set_curve methods")
            
            
            "Method 2: f_cop derived by curves"
            self.curve.sort_values("X", inplace = True)
            PLF_curve = np.array(self.curve["X"])
            f_COP_curve = np.array(self.curve["f_cop"])
            # f_COP = np.interp(PLF_PL, PLF_curve, f_COP_curve)
            
            self.f_COP = lambda x : np.interp(x, PLF_curve, f_COP_curve)

        
        elif self.plf_method == "C method":
            
            "Method 3: f_cop calculated"
            a=1/self.PLF_PL-1
            b=self.PLF_PL-1
            c=1/f_COP_model_FL-1
            X3=np.column_stack([a,b])
            
            model_reg_3 = linear_model.LinearRegression(fit_intercept = False).fit(X3,c)
            coeff_3 = model_reg_3.coef_
            coeff_0 = 1-coeff_3[0] -coeff_3[1]
                
            self.f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
            
    def calc_with_data_linear(self, df):
        
        # "Import data as Arrays"
        # SET = np.array(df["SET [°C]"])
        # Sfr = np.array(df["SFR [l/s]"])
        # LExT = np.array(df["LExT [°C]"])
        # HC = np.array(df["Heat Abs EVA [kW[]"])
        # PLF = np.array(df["PLF"])
        # X = np.column_stack([np.ones(len(HC)),SET,Sfr,LExT-SET,(LExT-SET)**2])
        
        PLF, COP, X = self.get_inputs_function(df)
        
        "Create matrix and calculations"
        if self.plf_method == "direct_linear":
            X_dir_lin = np.column_stack([X,PLF])
            COP_pred = self.model_reg.predict(X_dir_lin)
            
        elif self.plf_method == "direct_quadratic":
            X_dir_qua = np.column_stack([X,PLF,PLF**2]) 
            COP_pred = self.model_reg.predict(X_dir_qua)
        
        else:
            COP_pred = self.model_reg_FL.predict(X) * self.f_COP(PLF)
            
        return COP_pred
    
    def calc_with_data_exp(self, df):
        
        # "Import data as Arrays"
        # SET = np.array(df["SET [°C]"])
        # Sfr = np.array(df["SFR [l/s]"])
        # LExT = np.array(df["LExT [°C]"])
        # HC = np.array(df["Heat Abs EVA [kW[]"])
        # PLF = np.array(df["PLF"])
        # X = np.column_stack([np.ones(len(HC)),SET,Sfr,LExT-SET,(LExT-SET)**2])
        
        PLF, X, COP, A0 = self.get_inputs(df)
        
        "Create matrix and calculations"
        if self.plf_method == "direct_linear":
            COP_pred = self.f_method_d01(self.model_reg['x'], X)            
        elif self.plf_method == "direct_quadratic":
            COP_pred = self.f_method_d02(self.model_reg['x'], X) 
        else:
            COP_pred = self.f_method_n(self.model_reg['x'], X) * self.f_COP(PLF)
                
        return COP_pred
    
    def calc_with_data_COP(self, df):
        
                
        SET = np.array(df["SET [°C]"])
        LExT = np.array(df["LExT [°C]"])
        PLF = np.array(df["PLF"])
                
        COP_pred_FL = self.calc_COP_FL(LExT,SET)
        
        COP_pred = COP_pred_FL * self.f_COP(PLF)
        
        return COP_pred
    
    def test_with_catalogue(self):
              
        COP_pred_TOT = self.calc_with_data(self.df)
        COP_pred_FL = self.calc_with_data(self.df_FL)
        COP_pred_PL = self.calc_with_data(self.df_PL)
        
        KPI = {}
        KPI["TOT"] = {}
        KPI["PL"] = {}
        KPI["FL"] = {}
        
        KPI["FL"]["MAE_FL"]  = mean_absolute_error(self.df_FL["COP"], COP_pred_FL)
        KPI["FL"]["RMSE_FL"]  = root_mean_squared_error(self.df_FL["COP"], COP_pred_FL)
        KPI["FL"]["r2_FL"] = r2_score(self.df_FL["COP"], COP_pred_FL)
        
        KPI["PL"]["MAE_PL"]= mean_absolute_error(self.df_PL["COP"], COP_pred_PL)
        KPI["PL"]["RMSE_PL"] = root_mean_squared_error(self.df_PL["COP"], COP_pred_PL)
        KPI["PL"]["r2_PL"] = r2_score(self.df_PL["COP"], COP_pred_PL)
        
        KPI["TOT"]["MAE_TOT"] = mean_absolute_error(self.df["COP"], COP_pred_TOT)
        KPI["TOT"]["RMSE_TOT"] = root_mean_squared_error(self.df["COP"], COP_pred_TOT)
        KPI["TOT"]["r2_TOT"] = r2_score(self.df["COP"], COP_pred_TOT)
        
        return KPI
    

class model_h01(model_hp):
    def get_inputs_function(self, df):
        SET = np.array(df["SET [°C]"])
        Sfr = np.array(df["SFR [l/s]"])
        LExT = np.array(df["LExT [°C]"])
        HC = np.array(df["Heat Abs EVA [kW[]"])
        PLF = np.array(df["PLF"])
        COP = np.array(df["COP"])
        
        X = np.column_stack([np.ones(len(HC)),SET,Sfr,LExT-SET,(LExT-SET)**2])

        return PLF, COP, X
    
    def train_model(self,df):
        self.train_linear_model(df)
        
    def calc_with_data(self,df):
        return self.calc_with_data_linear(df)
    
class model_h02(model_hp):
    def get_inputs_function(self, df):
        SET = np.array(df["SET [°C]"])
        LExT = np.array(df["LExT [°C]"])
        HC = np.array(df["Heat Abs EVA [kW[]"])
        PLF = np.array(df["PLF"])
        COP = np.array(df["COP"])
        
        X = np.column_stack([np.ones(len(HC)),SET,LExT-SET,(LExT-SET)**2])

        return PLF, COP, X
    
    def train_model(self,df):
        self.train_linear_model(df)
    
    def calc_with_data(self,df):
        return self.calc_with_data_linear(df)

class model_h03(model_hp):
    def get_inputs_function(self, df):
        SET = np.array(df["SET [°C]"])
        Sfr = np.array(df["SFR [l/s]"])
        HC = np.array(df["Heat Abs EVA [kW[]"])
        PLF = np.array(df["PLF"])
        COP = np.array(df["COP"])
        
        X = np.column_stack([np.ones(len(HC)),SET,Sfr,SET**2])

        return PLF, COP, X
    
    def train_model(self,df):
        self.train_linear_model(df)
        
    def calc_with_data(self,df):
        return self.calc_with_data_linear(df)
        
class model_h04(model_hp):
    def get_inputs_function(self, df):
        SET = np.array(df["SET [°C]"])
        LExT = np.array(df["LExT [°C]"])
        HC = np.array(df["Heat Abs EVA [kW[]"])
        PLF = np.array(df["PLF"])
        COP = np.array(df["COP"])
        
        X = np.column_stack([np.ones(len(HC)), SET, LExT, LExT * SET])

        return PLF, COP, X
    
    def train_model(self,df):
        self.train_linear_model(df)
    
    def calc_with_data(self,df):
        return self.calc_with_data_linear(df)
    
class model_h05(model_hp):
    def get_inputs_function(self, df):
        SET = np.array(df["SET [°C]"])
        LET = np.array(df["LET [°C]"])
        HC = np.array(df["Heat Abs EVA [kW[]"])
        PLF = np.array(df["PLF"])
        COP = np.array(df["COP"])
        
        X = np.column_stack([np.ones(len(HC)), SET, LET, LET * SET])

        return PLF, COP, X
    
    def train_model(self,df):
        self.train_linear_model(df)
        
    def calc_with_data(self,df):
        return self.calc_with_data_linear(df)
    
class model_h06(model_hp):
        
    @staticmethod
    def f_method_d01(x0, xdata):
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]
        return Y_pred
    
    @staticmethod
    def f_method_d02(x0, xdata):
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]* xdata[:,2]**2 + x0[6]
        return Y_pred
    
    @staticmethod
    def f_method_n(x0, xdata):
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1]+ x0[4]
        return Y_pred        
    
    def get_inputs(self,df):
        SET = np.array(df["SET [°C]"])
        LET = np.array(df["LET [°C]"])
        PLF = np.array(df["PLF"])
        COP = np.array(df["COP"])
        
        "Create matrix and calculations"
        X = np.column_stack([SET, LET, PLF])
        if self.plf_method == "direct_linear":
            A0 = np.zeros(6)
        elif self.plf_method == "direct_quadratic":
            A0 = np.zeros(7)
        else:
            A0 = np.zeros(5)
        return PLF, X, COP, A0
    
    def train_model(self,df):
        self.train_exp_model(df)
        
    def calc_with_data(self,df):
        return self.calc_with_data_exp(df)
    
class model_h07(model_hp):
        
    @staticmethod
    def f_method_d01(x0, xdata):
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]
        return Y_pred
    
    @staticmethod
    def f_method_d02(x0, xdata):
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]* xdata[:,2]**2 + x0[6]
        return Y_pred
    
    @staticmethod
    def f_method_n(x0, xdata):
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1]+ x0[4]
        return Y_pred        
    
    def get_inputs(self,df):
        SET = np.array(df["SET [°C]"])
        LExT = np.array(df["LExT [°C]"])
        PLF = np.array(df["PLF"])
        COP = np.array(df["COP"])
        
        "Create matrix and calculations"
        X = np.column_stack([SET, LExT, PLF])
        if self.plf_method == "direct_linear":
            A0 = np.zeros(6)
        elif self.plf_method == "direct_quadratic":
            A0 = np.zeros(7)
        else:
            A0 = np.zeros(5)
        return PLF, X, COP, A0
    
    def train_model(self,df):
        self.train_exp_model(df)
        
    def calc_with_data(self,df):
        return self.calc_with_data_exp(df)
       
class model_h08(model_hp):
        
    @staticmethod
    def f_method_d01(x0, xdata):
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]
        return Y_pred
    
    @staticmethod
    def f_method_d02(x0, xdata):
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]* xdata[:,2]**2 + x0[6]
        return Y_pred
    
    @staticmethod
    def f_method_n(x0, xdata):
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1]+ x0[4]
        return Y_pred        
    
    def get_inputs(self,df):
        SExT = np.array(df["SExT [°C]"])
        LExT = np.array(df["LExT [°C]"])
        PLF = np.array(df["PLF"])
        COP = np.array(df["COP"])
        
        "Create matrix and calculations"
        X = np.column_stack([SExT, LExT, PLF])
        if self.plf_method == "direct_linear":
            A0 = np.zeros(6)
        elif self.plf_method == "direct_quadratic":
            A0 = np.zeros(7)
        else:
            A0 = np.zeros(5)
        return PLF, X, COP, A0
    
    def train_model(self,df):
        self.train_exp_model(df)
        
    def calc_with_data(self,df):
        return self.calc_with_data_exp(df)
    
class model_h09(model_hp):
        
    @staticmethod
    def f_method_d01(x0, xdata):
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]
        return Y_pred
    
    @staticmethod
    def f_method_d02(x0, xdata):
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]* xdata[:,2]**2 + x0[6]
        return Y_pred
    
    @staticmethod
    def f_method_n(x0, xdata):
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1]+ x0[4]
        return Y_pred        
    
    def get_inputs(self,df):
        SExT = np.array(df["SExT [°C]"])
        LET = np.array(df["LET [°C]"])
        PLF = np.array(df["PLF"])
        COP = np.array(df["COP"])
        
        "Create matrix and calculations"
        X = np.column_stack([SExT, LET, PLF])
        if self.plf_method == "direct_linear":
            A0 = np.zeros(6)
        elif self.plf_method == "direct_quadratic":
            A0 = np.zeros(7)
        else:
            A0 = np.zeros(5)
        return PLF, X, COP, A0
    
    def train_model(self,df):
        self.train_exp_model(df)
        
    def calc_with_data(self,df):
        return self.calc_with_data_exp(df)
    
class model_h10(model_hp):
        
    allowed_plf_methods = [
            "ISO 13612-2 mod A",
            "ISO 13612-2 mod B",
            "C method"
            ]
    
    def __init__(self, plf_method = "ISO 13612-2 mod A"):
        super().__init__(plf_method = plf_method)
        
    def calc_COP_FL(self, LExT, SET):
        COP_carnot = (273+ LExT)/(LExT - SET)
        COP_carnot[LExT <= SET] = 50
        return COP_carnot * self.eta_design
    
    def train_model(self,df,*args,**kwargs):
        self.train_COP_model(df,*args,**kwargs)
        
    def calc_with_data(self,df):
        return self.calc_with_data_COP(df)
    
class model_h11(model_hp):
        
    allowed_plf_methods = [
            "ISO 13612-2 mod A",
            "ISO 13612-2 mod B",
            "C method"
            ]
    
    def __init__(self, plf_method = "ISO 13612-2 mod A"):
        super().__init__(plf_method = plf_method)
        
    def calc_COP_FL(self, LExT, SET):
        den = np.maximum((LExT - SET),18)
        COP_carnot = (273+ LExT)/den
        return COP_carnot * self.eta_design
    
    def train_model(self,df,*args,**kwargs):
        self.train_COP_model(df,*args,**kwargs)
        
    def calc_with_data(self,df):
        return self.calc_with_data_COP(df)
    
class model_h12(model_hp):
        
    allowed_plf_methods = [
            "ISO 13612-2 mod A",
            "ISO 13612-2 mod B",
            "C method"
            ]
    
    def __init__(self, plf_method = "ISO 13612-2 mod A"):
        super().__init__(plf_method = plf_method)
        
    def calc_COP_FL(self, LExT, SET):
        
        
        den_1 = np.maximum((LExT - SET),1)
        COP_carnot_1 = (273+ LExT)/den_1
        COP_carnot_2 = (273+ LExT)/den_1
        
        COP_carnot_non_filt = (273+ LExT)/(LExT - SET)
        
        COP_carnot_2[LExT > SET] = COP_carnot_non_filt[LExT > SET]
        
        COP_carnot = np.minimum(COP_carnot_1, COP_carnot_2)
        
        eta = self.eta_design / (
            self.eta_design*(1-COP_carnot/COP_carnot_non_filt)\
            + COP_carnot/COP_carnot_non_filt 
            )
        
        return COP_carnot * eta
    
    def train_model(self,df,*args,**kwargs):
        self.train_COP_model(df,*args,**kwargs)
        
    def calc_with_data(self,df):
        return self.calc_with_data_COP(df)

#%% H11N-----------------------------------------------------------------------

def model_h11n(df, curve, design_point_T = (7,35), indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    "Divide between part load and full load operative points"
    df_PL= df[df['PLF']!=1]
    

    "Carnot efficency full load calculations" 
    SET_data = design_point_T[0] #[°C]
    LExT_data = design_point_T[1] #[°C]
    curve = curve.set_index(curve['SET'])
    COP_data = curve.loc[SET_data, 'COP_fl']
    COP_carnot = (LExT_data + 273.15 )/ (LExT_data - SET_data)
    eta_FL = COP_data / COP_carnot # second principle efficency for full load data point
       
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLF_PL = np.array(df_PL["PLF"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create function to calculate COP_FL_pred" 
    X=np.column_stack([SET_PL, LExT_PL, COP_PL])
    
    def COP_fun(x, y):
        
        SET_PL = x[:, 0]
        LExT_PL = x[:, 1]
        COP_carnot_PL=np.ones(len(SET_PL))
        COP_FL_pred=np.ones(len(SET_PL))
        
        for i in range(len(LExT_PL)):
            COP_carnot_PL[i] = (273+ LExT_PL[i])/max((LExT_PL[i] - SET_PL[i]),18)
            COP_FL_pred[i] = COP_carnot_PL[i] * eta_FL
            
        return COP_FL_pred    
    
    COP_pred_FL = lambda x, y:  COP_fun(x, y)   
    f_COP_model_FL = COP_PL/ COP_pred_FL (X, eta_FL)
   
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"       
        def f_COP_fun(x):
            
            if not isinstance(x,np.ndarray):
                x = np.array([x])
            f_COP=np.ones(len(x))
            
            for i in range(len(x)):
                if  x[i] >= 0.25:
                    f_COP[i]=1;
                else:
                    f_COP[i]=x[i]/(0.9*4*x[i]+0.1)
            return f_COP
                
        f_COP = lambda x : f_COP_fun(x)
        
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"       
        curve.sort_values("X", inplace = True)
        PLF_curve = np.array(curve["X"])
        f_COP_curve = np.array(curve["f_cop"])
        # f_COP = np.interp(PLF_PL, PLF_curve, f_COP_curve)
        
        f_COP = lambda x : np.interp(x, PLF_curve, f_COP_curve)

    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        
        a=1/PLF_PL-1
        b=PLF_PL-1
        c=1/f_COP_model_FL-1
        X3=np.column_stack([a,b])
        
        model_reg_3 = linear_model.LinearRegression(fit_intercept = False).fit(X3,c)
        coeff_3 = model_reg_3.coef_
        coeff_0 = 1-coeff_3[0] -coeff_3[1]
            
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "Carnot efficency": eta_FL,
        "COP_pred_FL":  COP_pred_FL,
        "F_COP": f_COP,
        }

#%% H12N-----------------------------------------------------------------------

def model_h12n(df, curve, design_point_T = (7,35), indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    "Divide between part load and full load operative points"
    df_PL= df[df['PLF']!=1]
    

    "Carnot efficency full load calculations"
        
    SET_data = design_point_T[0] #[°C]
    LExT_data = design_point_T[1] #[°C]
    curve = curve.set_index(curve['SET'])
    COP_data = curve.loc[SET_data, 'COP_fl']
    COP_carnot = (LExT_data + 273.15 )/ (LExT_data - SET_data)
    eta_FL = COP_data / COP_carnot # second principle efficency for full load data point
       
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLF_PL = np.array(df_PL["PLF"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create function to calculate COP_FL_pred" 
    X=np.column_stack([SET_PL, LExT_PL, COP_PL])
    
    def COP_fun(x, y, z): 
        
        SET_PL = x[:, 0]
        LExT_PL = x[:, 1]
        eta = np.ones(len(SET_PL))
        COP_carnot_PL1 = np.ones(len(SET_PL))
        COP_carnot_PL2 = np.ones(len(SET_PL))
        COP_carnot_PL =  np.ones(len(SET_PL))
        
        for i in range(len(LExT_PL)):
            
            COP_carnot_PL1[i] = (273+ LExT_PL[i])/max((LExT_PL[i] - SET_PL[i]),1)
            if LExT_PL[i] > SET_PL[i]:
                
               COP_carnot_PL2[i] = (273+ LExT_PL[i])/(LExT_PL[i] - SET_PL[i])
            else:
                COP_carnot_PL2[i] = (273+ LExT_PL[i])/max((LExT_PL[i] - SET_PL[i]),1)
                
            COP_carnot_PL[i] = min(COP_carnot_PL1[i],  COP_carnot_PL2[i])
            eta[i] = y/ (y*(1-COP_carnot_PL[i]/z) + COP_carnot_PL[i]/z )
        
        COP_pred_FL = eta* COP_carnot_PL
      
        
        return  COP_pred_FL   
    
    COP_pred_FL = lambda x, y, z: COP_fun(x, y, z)  
    f_COP_model_FL = COP_PL/ COP_pred_FL(X, eta_FL, COP_carnot)
   
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        def f_COP_fun(x):
            
            if not isinstance(x,np.ndarray):
                x = np.array([x])
            f_COP=np.ones(len(x))
            
            for i in range(len(x)):
                if  x[i] >= 0.25:
                    f_COP[i]=1;
                else:
                    f_COP[i]=x[i]/(0.9*4*x[i]+0.1)
            return f_COP
                
        f_COP = lambda x : f_COP_fun(x)
        
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        
        curve.sort_values("X", inplace = True)
        PLF_curve = np.array(curve["X"])
        f_COP_curve = np.array(curve["f_cop"])
        
        f_COP = lambda x : np.interp(x, PLF_curve, f_COP_curve)

    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        
        a=1/PLF_PL-1
        b=PLF_PL-1
        c=1/f_COP_model_FL-1
        X3=np.column_stack([a,b])
        
        model_reg_3 = linear_model.LinearRegression(fit_intercept = False).fit(X3,c)
        coeff_3 = model_reg_3.coef_
        coeff_0 = 1-coeff_3[0] -coeff_3[1]
            
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "Carnot efficency": eta_FL,
        "COP_Carnot": COP_carnot,
        "COP_pred_FL": COP_pred_FL,
        "F_COP": f_COP,
        "Debug": f_COP(PLF_PL),
        }

#%% Load Models----------------------------------------------------------------

def load_models(df, curve):
    
    Model={}
    
    #%% H01D01-----------------------------------------------------------------
    
    Model['H01D01']  = model_h01d01(df)
     
    #%% H01D02-----------------------------------------------------------------
    
    Model['H01D02'] = model_h01d02(df)
    
    #%% H10N-------------------------------------------------------------------
    
    Model['H01N - mod A'] = model_h01n(df, curve, indirect_model = "ISO 13612-2 mod A")
    Model['H01N - mod B'] = model_h01n(df, curve, indirect_model = "ISO 13612-2 mod B")
    Model['H01N - mod C'] = model_h01n(df, curve, indirect_model = "C method")
     
    #%% H02D01-----------------------------------------------------------------
    
    Model['H02D01'] = model_h02d01(df)
    
    #%% H02D02-----------------------------------------------------------------
    
    Model['H02D02'] = model_h02d02(df)
    
    #%% H02N-------------------------------------------------------------------
    
    Model['H02N - mod A'] = model_h02n(df, curve, indirect_model = "ISO 13612-2 mod A")
    Model['H02N - mod B'] = model_h02n(df, curve, indirect_model = "ISO 13612-2 mod B")  
    Model['H02N - mod C'] = model_h02n(df, curve, indirect_model = "C method")
     
    #%% H03D01-----------------------------------------------------------------
    
    Model['H03D01'] = model_h03d01(df)
    
    #%% H03D02-----------------------------------------------------------------
    
    Model['H03D02'] = model_h03d02(df)
    
    #%% H03N-------------------------------------------------------------------
    
    Model['H03N - mod A'] = model_h03n(df, curve, indirect_model = "ISO 13612-2 mod A")
    Model['H03N - mod B'] = model_h03n(df, curve, indirect_model = "ISO 13612-2 mod B")  
    Model['H03N - mod C'] = model_h03n(df, curve, indirect_model = "C method")
    
    #%% H04D01-----------------------------------------------------------------
    
    Model['H04D01'] = model_h04d01(df)
    
    #%% H04D02-----------------------------------------------------------------
    
    Model['H04D02'] = model_h04d02(df)
    
    #%% H04N-------------------------------------------------------------------
    
    Model['H04N - mod A'] = model_h04n(df, curve, indirect_model = "ISO 13612-2 mod A")
    Model['H04N - mod B'] = model_h04n(df, curve, indirect_model = "ISO 13612-2 mod B")  
    Model['H04N - mod C'] = model_h04n(df, curve, indirect_model = "C method")
    
    #%% H05D01-----------------------------------------------------------------
    
    Model['H05D01'] = model_h05d01(df)
    
    #%% H05D02-----------------------------------------------------------------
    
    Model['H05D02'] = model_h05d02(df)
    
    #%% H05N-------------------------------------------------------------------
    
    Model['H05N - mod A'] = model_h05n(df, curve, indirect_model = "ISO 13612-2 mod A")
    Model['H05N - mod B'] = model_h05n(df, curve, indirect_model = "ISO 13612-2 mod B")  
    Model['H05N - mod C'] = model_h05n(df, curve, indirect_model = "C method")
    
    #%% H06D01-----------------------------------------------------------------
    
    Model['H06D01'] = model_h06d01(df)
    
    #%% H06D02-----------------------------------------------------------------
    
    Model['H06D02'] = model_h06d02(df)
    
    #%% H05N-------------------------------------------------------------------
    
    Model['H05N - mod A'] = model_h05n(df, curve, indirect_model = "ISO 13612-2 mod A")
    Model['H05N - mod B'] = model_h05n(df, curve, indirect_model = "ISO 13612-2 mod B")  
    Model['H05N - mod C'] = model_h05n(df, curve, indirect_model = "C method")
    
    
    
    #%% H06N-------------------------------------------------------------------
    
    Model['H06N - mod A'] = model_h06n(df, curve, indirect_model = "ISO 13612-2 mod A")
    Model['H06N - mod B'] = model_h06n(df, curve, indirect_model = "ISO 13612-2 mod B")  
    Model['H06N - mod C'] = model_h06n(df, curve, indirect_model = "C method")
    
    #%% H07D01-----------------------------------------------------------------
    
    Model['H07D01'] = model_h07d01(df)
    
    #%% H07D02-----------------------------------------------------------------
    
    Model['H07D02'] = model_h07d02(df)
    
    #%% H07N-------------------------------------------------------------------
    
    Model['H07N - mod A'] = model_h07n(df, curve, indirect_model = "ISO 13612-2 mod A")
    Model['H07N - mod B'] = model_h07n(df, curve, indirect_model = "ISO 13612-2 mod B")  
    Model['H07N - mod C'] = model_h07n(df, curve, indirect_model = "C method")
    
    #%% H08D01-----------------------------------------------------------------
    
    Model['H08D01'] = model_h08d01(df)
    
    #%% H08D02-----------------------------------------------------------------
    
    Model['H08D02'] = model_h08d02(df)
    
    #%% H08N-------------------------------------------------------------------
    
    Model['H08N - mod A'] = model_h08n(df, curve, indirect_model = "ISO 13612-2 mod A")
    Model['H08N - mod B'] = model_h08n(df, curve, indirect_model = "ISO 13612-2 mod B")  
    Model['H08N - mod C'] = model_h08n(df, curve, indirect_model = "C method")
    
    #%% H09D01-----------------------------------------------------------------
    
    Model['H09D01'] = model_h09d01(df)
    
    #%% H09D02-----------------------------------------------------------------
    
    Model['H09D02'] = model_h09d02(df)
    
    #%% H09N-------------------------------------------------------------------
    
    Model['H09N - mod A'] = model_h09n(df, curve, indirect_model = "ISO 13612-2 mod A")
    Model['H09N - mod B'] = model_h09n(df, curve, indirect_model = "ISO 13612-2 mod B")  
    Model['H09N - mod C'] = model_h09n(df, curve, indirect_model = "C method")
    
    #%% H10N-------------------------------------------------------------------
    
    Model['H10N - mod A'] = model_h10n(df, curve, indirect_model = "ISO 13612-2 mod A")
    Model['H10N - mod B'] = model_h10n(df, curve, indirect_model = "ISO 13612-2 mod B")  
    Model['H10N - mod C'] = model_h10n(df, curve, indirect_model = "C method")
    
    #%% H11N-------------------------------------------------------------------
    
    Model['H11N - mod A'] = model_h11n(df, curve, indirect_model = "ISO 13612-2 mod A")
    Model['H11N - mod B'] = model_h11n(df, curve, indirect_model = "ISO 13612-2 mod B")  
    Model['H11N - mod C'] = model_h11n(df, curve, indirect_model = "C method")
    
    #%% H12N-------------------------------------------------------------------
    
    Model['H12N - mod A'] = model_h12n(df, curve, indirect_model = "ISO 13612-2 mod A")
    Model['H12N - mod B'] = model_h12n(df, curve, indirect_model = "ISO 13612-2 mod B")  
    Model['H12N - mod C'] = model_h12n(df, curve, indirect_model = "C method")
    
    return Model





















































