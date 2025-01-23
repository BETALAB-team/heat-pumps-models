import copy

import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error, root_mean_squared_error,r2_score,mean_absolute_percentage_error
from scipy.optimize import minimize


class model_hp():
    
    allowed_plr_methods = [
            "direct_linear",
            "direct_quadratic",
            "ISO 13612-2 mod A",
            "ISO 13612-2 mod B",
            "method C"
            ]
    
    def __init__(self, plr_method = "direct_linear"):
        
        #INIT: Create object of class model_hp and create as
        #an attribute plr_method
        
        if plr_method not in self.allowed_plr_methods:
            raise TypeError(f"plr_method must be chosen from the following list: {self.allowed_plr_methods}")
        
        self.plr_method = plr_method
        
    def set_curve_df(self,curve):
        
        #METHOD: import curve of points defined by normative ISO EN 14825
        self.curve = copy.deepcopy(curve)
        
    def train_linear_model(self,df): 
        
        #METHOD: train all the model of the linear model type
        self.df = df
        df_FL = df[df['PLR']==1]
        df_PL = df[df['PLR']!=1]
        
        self.df_FL = df_FL
        self.df_PL = df_PL
        

        #Get_inputs_function is defined in each model class
        self.PLR, self.COP, self.X = self.get_inputs_function(self.df)
        self.PLR_PL, self.COP_PL, self.X_PL = self.get_inputs_function(self.df_PL)
        self.PLR_FL, self.COP_FL, self.X_FL = self.get_inputs_function(self.df_FL)
      
        #Create matrix and full load calculations
        self.model_reg_FL = linear_model.LinearRegression().fit(self.X_FL, self.COP_FL)
        
        #Create matrix and part load calculations
        COP_FL_pred = self.model_reg_FL.predict(self.X_PL)
        f_COP_model_FL = self.COP_PL/COP_FL_pred
        

        #Create matrix and calculations
        if self.plr_method == "direct_linear":
            X_dir_lin = np.column_stack([self.X,self.PLR])
            self.model_reg = linear_model.LinearRegression().fit(X_dir_lin, self.COP)
            
        elif self.plr_method == "direct_quadratic":
            X_dir_qua = np.column_stack([self.X,self.PLR,self.PLR**2])   
            self.model_reg = linear_model.LinearRegression().fit(X_dir_qua, self.COP)
        else:
            self.calculate_f_cop()
            
    def train_exp_model(self,df):
        
        #METHOD: train all the model of the exponential model type
        self.df = df
        self.df_FL = df[df['PLR']==1]
        self.df_PL = df[df['PLR']!=1]
        
        #Get_inputs_function is defined in each model class
        self.PLR, self.X, self.COP, self.A0 = self.get_inputs(self.df)
        self.PLR_PL, self.X_PL, self.COP_PL, self.A0_PL = self.get_inputs(self.df_PL)
        self.PLR_FL, self.X_FL, self.COP_FL, self.A0_FL = self.get_inputs(self.df_FL)
        
        #METHOD: define the residuals of a specific type of plr_method.
        #The f_method is defined directly inside the class of the specifc model  
        def fun(x0,xdata,ydata):
            fun_m = {
                    "direct_linear":self.f_method_d01,
                    "direct_quadratic":self.f_method_d02,
                    "ISO 13612-2 mod A":self.f_method_n,
                    "ISO 13612-2 mod B":self.f_method_n,
                    "method C":self.f_method_n,
                }[self.plr_method]
            Y_pred = fun_m(x0,xdata)
            return sum((Y_pred-ydata)**2)
        

        #Select the minimization procedure depending on the type of plr_method.
        if self.plr_method in ["direct_linear","direct_quadratic"]:
            self.model_reg = minimize(fun, self.A0, args = (self.X, self.COP), method = 'L-BFGS-B')   
        else:
            self.model_reg = minimize(fun, self.A0, args = (self.X_FL, self.COP_FL), method = 'L-BFGS-B')
            A = self.model_reg['x']
            COP_FL_pred = A[0]*np.exp(A[1]*self.X_PL[:,0] + A[2]*self.X_PL[:,1]) + A[3]*self.X_PL[:,0]/self.X_PL[:,1] + A[4]    
            f_COP_model_FL = self.COP_PL/COP_FL_pred
            self.calculate_f_cop()
        
    def train_COP_model(self, df, Source_T = 7, Load_T = 35, COP = None):
        
        #METHOD: train all the model of the Carnot model type
        self.df = df

        self.df_FL = df[df['PLR']==1]
        self.df_PL = df[df['PLR']!=1]
        self.PLR_PL = np.array(self.df_PL["PLR"])
        
        self.COP_carnot = (Load_T + 273.15 )/ (Load_T - Source_T)
        
        #Check if model has the required curve uploaded
        if hasattr(self, "curve"):
            curve = copy.deepcopy(self.curve)
            curve = curve.set_index(curve['SET'])  
            COP = curve.loc[Source_T, 'COP_fl'] 
            self.eta_design = COP / self.COP_carnot # second principle efficency for full load data point
        else:
            if COP == None:
                raise ValueError("If no design points curve df has been set, COP at design load must be provided")
            self.eta_design = COP / self.COP_carnot     
        
        SET_PL = np.array(self.df_PL["SET [°C]"])
        LExT_PL = np.array(self.df_PL["LExT [°C]"])
        COP_PL = np.array(self.df_PL["COP"])
                
        COP_pred_PL = self.calc_COP_FL(LExT_PL, SET_PL)
        
        f_COP_model_FL = COP_PL/COP_pred_PL
        
        self.calculate_f_cop()
        
    def calculate_f_cop(self):
        if self.plr_method == "ISO 13612-2 mod A":
            
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
            
                
        elif self.plr_method == "ISO 13612-2 mod B":
            if not hasattr(self, 'curve'):
                PLR_curve = np.array([0,0.153846154,0.346153846,0.538461538,0.884615385,1])
                f_COP_curve = np.array([0,1.763963705,1.46640949,1.361503767,1.051338345,1])        
            else:
                "Method 2: f_cop derived by curves"
                self.curve.sort_values("X", inplace = True)
                PLR_curve = np.array(self.curve["X"])
                f_COP_curve = np.array(self.curve["f_cop"])
                # f_COP = np.interp(PLR_PL, PLR_curve, f_COP_curve)
            
            self.f_COP = lambda x : np.interp(x, PLR_curve, f_COP_curve)

        
        elif self.plr_method == "method C":
            
            "Method 3: f_cop calculated"
            if not hasattr(self, 'curve'):
                PLR_curve = np.array([0,0.153846154,0.346153846,0.538461538,0.884615385,1])
                f_COP_curve = np.array([0,1.763963705,1.46640949,1.361503767,1.051338345,1])     
            else:
                self.curve.sort_values("X", inplace = True)
                PLR_curve = np.array(self.curve["X"])
                f_COP_curve = np.array(self.curve["f_cop"])
            PLR_curve = np.delete(PLR_curve,[0,5])
            f_COP_curve = np.delete(f_COP_curve,[0,5])
            a=1/PLR_curve-1
            b=PLR_curve-1
            c=1/f_COP_curve-1
            X3=np.column_stack([a,b])
            
            model_reg_3 = linear_model.LinearRegression(fit_intercept = False).fit(X3,c)
            coeff_3 = model_reg_3.coef_
            coeff_0 = 1-coeff_3[0] -coeff_3[1]
                
            self.f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
            
    def calc_with_data_linear(self, df):

        PLR, COP, X = self.get_inputs_function(df)
        
        "Create matrix and calculations"
        if self.plr_method == "direct_linear":
            X_dir_lin = np.column_stack([X,PLR])
            COP_pred = self.model_reg.predict(X_dir_lin)
            
        elif self.plr_method == "direct_quadratic":
            X_dir_qua = np.column_stack([X,PLR,PLR**2]) 
            COP_pred = self.model_reg.predict(X_dir_qua)
        
        else:
            COP_pred = self.model_reg_FL.predict(X) * self.f_COP(PLR)
            
        return COP_pred
    
    def calc_with_data_exp(self, df):
        
        PLR, X, COP, A0 = self.get_inputs(df)
        
        "Create matrix and calculations"
        if self.plr_method == "direct_linear":
            COP_pred = self.f_method_d01(self.model_reg['x'], X)            
        elif self.plr_method == "direct_quadratic":
            COP_pred = self.f_method_d02(self.model_reg['x'], X) 
        else:
            COP_pred = self.f_method_n(self.model_reg['x'], X) * self.f_COP(PLR)
                
        return COP_pred
    
    def calc_with_data_COP(self, df):
        
                
        SET = np.array(df["SET [°C]"])
        LExT = np.array(df["LExT [°C]"])
        PLR = np.array(df["PLR"])
                
        COP_pred_FL = self.calc_COP_FL(LExT,SET)
        
        COP_pred = COP_pred_FL * self.f_COP(PLR)
        
        return COP_pred
    
    def test_with_catalogue(self):
              
        COP_pred_TOT = self.calc_with_data(self.df)
        COP_pred_FL = self.calc_with_data(self.df_FL)
        COP_pred_PL = self.calc_with_data(self.df_PL)
        
        KPI = {}
        KPI["TOT"] = {}
        KPI["PL"] = {}
        KPI["FL"] = {}
        
        KPI["FL"]["MAPE_FL"]  = mean_absolute_percentage_error(self.df_FL["COP"], COP_pred_FL)
        KPI["FL"]["RMSE_FL"]  = root_mean_squared_error(self.df_FL["COP"], COP_pred_FL)
        KPI["FL"]["r2_FL"] = r2_score(self.df_FL["COP"], COP_pred_FL)
        
        KPI["PL"]["MAPE_PL"]= mean_absolute_percentage_error(self.df_PL["COP"], COP_pred_PL)
        KPI["PL"]["RMSE_PL"] = root_mean_squared_error(self.df_PL["COP"], COP_pred_PL)
        KPI["PL"]["r2_PL"] = r2_score(self.df_PL["COP"], COP_pred_PL)
        
        KPI["TOT"]["MAPE_TOT"] = mean_absolute_percentage_error(self.df["COP"], COP_pred_TOT)
        KPI["TOT"]["RMSE_TOT"] = root_mean_squared_error(self.df["COP"], COP_pred_TOT)
        KPI["TOT"]["r2_TOT"] = r2_score(self.df["COP"], COP_pred_TOT)
        
        return KPI
    
    def test_with_data(self, df_real_data):
        
        COP_pred = self.calc_with_data(df_real_data)
        
        KPI = {}
        KPI["TOT"] = {}
        
        KPI["TOT"]["MAPE_TOT"] = mean_absolute_percentage_error(df_real_data["COP"], COP_pred)
        KPI["TOT"]["RMSE_TOT"] = root_mean_squared_error(df_real_data["COP"], COP_pred)
        KPI["TOT"]["r2_TOT"] = r2_score(df_real_data["COP"], COP_pred)
        
        return KPI
    
    def calc_SCOP(self,df_real_data):
        
        COP_pred = self.calc_with_data(df_real_data)
        SCOP = np.sum(np.multiply(COP_pred, df_real_data["Pow [kW]"]))/np.sum(df_real_data["Pow [kW]"])
        # SCOP = ct(np.multiply(COP_pred,df_real_data["Pow [kW]"]),df_real_data["Time [min]"])/ct(np.multiply(COP_pred,df_real_data["Pow [kW]"]))
        return SCOP

    

class model_h01(model_hp):
    def get_inputs_function(self, df):
        SET = np.array(df["SET [°C]"])
        Sfr = np.array(df["SFR [kg/s]"])
        LExT = np.array(df["LExT [°C]"])
        PLR = np.array(df["PLR"])
        COP = np.array(df["COP"])
        
        X = np.column_stack([np.ones(len(SET)),SET,Sfr,LExT-SET,(LExT-SET)**2])

        return PLR, COP, X
    
    def train_model(self,df):
        self.train_linear_model(df)
        
    def calc_with_data(self,df):
        return self.calc_with_data_linear(df)
    
class model_h02(model_hp):
    def get_inputs_function(self, df):
        SET = np.array(df["SET [°C]"])
        LExT = np.array(df["LExT [°C]"])
        PLR = np.array(df["PLR"])
        COP = np.array(df["COP"])
        
        X = np.column_stack([np.ones(len(SET)),SET,LExT-SET,(LExT-SET)**2])

        return PLR, COP, X
    
    def train_model(self,df):
        self.train_linear_model(df)
    
    def calc_with_data(self,df):
        return self.calc_with_data_linear(df)

class model_h03(model_hp):
    def get_inputs_function(self, df):
        SET = np.array(df["SET [°C]"])
        Sfr = np.array(df["SFR [kg/s]"])
        PLR = np.array(df["PLR"])
        COP = np.array(df["COP"])
        
        X = np.column_stack([np.ones(len(SET)),SET,Sfr,SET**2])

        return PLR, COP, X
    
    def train_model(self,df):
        self.train_linear_model(df)
        
    def calc_with_data(self,df):
        return self.calc_with_data_linear(df)
        
class model_h04(model_hp):
    def get_inputs_function(self, df):
        SET = np.array(df["SET [°C]"])
        LExT = np.array(df["LExT [°C]"])
        PLR = np.array(df["PLR"])
        COP = np.array(df["COP"])
        
        X = np.column_stack([np.ones(len(SET)), SET, LExT, LExT * SET])

        return PLR, COP, X
    
    def train_model(self,df):
        self.train_linear_model(df)
    
    def calc_with_data(self,df):
        return self.calc_with_data_linear(df)
    
class model_h05(model_hp):
    def get_inputs_function(self, df):
        SET = np.array(df["SET [°C]"])
        LET = np.array(df["LET [°C]"])
        PLR = np.array(df["PLR"])
        COP = np.array(df["COP"])
        
        X = np.column_stack([np.ones(len(SET)), SET, LET, LET * SET])

        return PLR, COP, X
    
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
        PLR = np.array(df["PLR"])
        COP = np.array(df["COP"])
        
        "Create matrix and calculations"
        X = np.column_stack([SET, LET, PLR])
        if self.plr_method == "direct_linear":
            A0 = np.zeros(6)
        elif self.plr_method == "direct_quadratic":
            A0 = np.zeros(7)
        else:
            A0 = np.zeros(5)
        return PLR, X, COP, A0
    
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
        PLR = np.array(df["PLR"])
        COP = np.array(df["COP"])
        
        "Create matrix and calculations"
        X = np.column_stack([SET, LExT, PLR])
        if self.plr_method == "direct_linear":
            A0 = np.zeros(6)
        elif self.plr_method == "direct_quadratic":
            A0 = np.zeros(7)
        else:
            A0 = np.zeros(5)
        return PLR, X, COP, A0
    
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
        PLR = np.array(df["PLR"])
        COP = np.array(df["COP"])
        
        "Create matrix and calculations"
        X = np.column_stack([SExT, LExT, PLR])
        if self.plr_method == "direct_linear":
            A0 = np.zeros(6)
        elif self.plr_method == "direct_quadratic":
            A0 = np.zeros(7)
        else:
            A0 = np.zeros(5)
        return PLR, X, COP, A0
    
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
        PLR = np.array(df["PLR"])
        COP = np.array(df["COP"])
        
        "Create matrix and calculations"
        X = np.column_stack([SExT, LET, PLR])
        if self.plr_method == "direct_linear":
            A0 = np.zeros(6)
        elif self.plr_method == "direct_quadratic":
            A0 = np.zeros(7)
        else:
            A0 = np.zeros(5)
        return PLR, X, COP, A0
    
    def train_model(self,df):
        self.train_exp_model(df)
        
    def calc_with_data(self,df):
        return self.calc_with_data_exp(df)
    
class model_h10(model_hp):
        
    allowed_plr_methods = [
            "ISO 13612-2 mod A",
            "ISO 13612-2 mod B",
            "method C"
            ]
    
    def __init__(self, plr_method = "ISO 13612-2 mod A"):
        super().__init__(plr_method = plr_method)
        
    def calc_COP_FL(self, LExT, SET):
        COP_carnot = (273+ LExT)/(LExT - SET)
        COP_carnot[LExT <= SET] = 50
        return COP_carnot * self.eta_design
    
    def train_model(self,df,*args,**kwargs):
        self.train_COP_model(df,*args,**kwargs)
        
    def calc_with_data(self,df):
        return self.calc_with_data_COP(df)
    
class model_h11(model_hp):
        
    allowed_plr_methods = [
            "ISO 13612-2 mod A",
            "ISO 13612-2 mod B",
            "method C"
            ]
    
    def __init__(self, plr_method = "ISO 13612-2 mod A"):
        super().__init__(plr_method = plr_method)
        
    def calc_COP_FL(self, LExT, SET):
        den = np.maximum((LExT - SET),18)
        COP_carnot = (273+ LExT)/den
        return COP_carnot * self.eta_design
    
    def train_model(self,df,*args,**kwargs):
        self.train_COP_model(df,*args,**kwargs)
        
    def calc_with_data(self,df):
        return self.calc_with_data_COP(df)
    
class model_h12(model_hp):
        
    allowed_plr_methods = [
            "ISO 13612-2 mod A",
            "ISO 13612-2 mod B",
            "method C"
            ]
    
    def __init__(self, plr_method = "ISO 13612-2 mod A"):
        super().__init__(plr_method = plr_method)
        
    def calc_COP_FL(self, LExT, SET):
        
        
        den_1 = np.maximum((LExT - SET),1)
        COP_carnot_1 = (273+ LExT)/den_1
        COP_carnot_2 = (273+ LExT)/den_1
        
        COP_carnot_non_filt = (273+ LExT)/(LExT - SET)
        
        COP_carnot_2[LExT > SET] = COP_carnot_non_filt[LExT > SET]
        
        COP_carnot = np.minimum(COP_carnot_1, COP_carnot_2)
        
        eta = self.eta_design / (
            self.eta_design*(1-COP_carnot/self.COP_carnot)\
            + COP_carnot/self.COP_carnot
            )
        
        return COP_carnot * eta
    
    def train_model(self,df,*args,**kwargs):
        self.train_COP_model(df,*args,**kwargs)
        
    def calc_with_data(self,df):
        return self.calc_with_data_COP(df)







