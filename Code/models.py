import numpy as np
from sklearn import linear_model
from scipy.optimize import minimize

#%% H01D01---------------------------------------------------------------------

def model_h01d01(df):
    
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    Sfr = np.array(df["SFR [kg/s]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP = np.array(df["COP"])
    
    "Create matrix and calculations"
    X = np.column_stack([np.ones(len(PLR)),SET,Sfr,LExT-SET,(LExT-SET)**2,PLR])
    model_reg = linear_model.LinearRegression().fit(X, COP)
    
       
    return {"scikit model": model_reg}

#%%H01D02----------------------------------------------------------------------

def model_h01d02(df):
    
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    Sfr = np.array(df["SFR [kg/s]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP = np.array(df["COP"])

    "Create matrix and calculations"
    X = np.column_stack([np.ones(len(PLR)),SET,Sfr,LExT-SET,(LExT-SET)**2,PLR, PLR**2])   
    model_reg = linear_model.LinearRegression().fit(X, COP)
    
    return {"scikit model": model_reg}

#%%H01N------------------------------------------------------------------------

def model_h01n(df, curve, source, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    if source not in ["Air","Water"]:
        raise TypeError("source must be chosen from the following list: \"Water\", \"Air\"")
        
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1]
    
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    Sfr_FL = np.array(df_FL["SFR [kg/s]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([np.ones(len(SET_FL)),SET_FL,Sfr_FL,LExT_FL-SET_FL,(LExT_FL-SET_FL)**2])
    model_reg_FL = linear_model.LinearRegression().fit(X_FL, COP_FL)
    
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    Sfr_PL = np.array(df_PL["SFR [kg/s]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    X_PL = np.column_stack([np.ones(len(SET_PL)),SET_PL,Sfr_PL,LExT_PL-SET_PL,(LExT_PL-SET_PL)**2])
    COP_FL_pred = model_reg_FL.predict(X_PL)
    f_COP_model_FL = COP_PL/COP_FL_pred
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
       
        def f_COP_fun(x):
            if not isinstance(x,np.ndarray):
                x = np.array(x)
            f_COP=np.ones(len(x))
            for i in range(len(x)):
                if  x[i] >= 0.25:
                    f_COP[i]=1;
                else:
                    if source =="Water":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)
                    elif source == "Air":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)*(1-0.25*(1-x[i]*4))
            return f_COP
                
        f_COP = lambda x : f_COP_fun(x)
        
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        curve.sort_values("X", inplace = True)
        PLR_curve = np.array(curve["X"])
        f_COP_curve = np.array(curve["f_cop"])
        
        f_COP = lambda x : np.interp(x, PLR_curve, f_COP_curve)

    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        a=1/PLR_PL-1
        b=PLR_PL-1
        c=1/f_COP_model_FL-1
        X3=np.column_stack([a,b])
        
        model_reg_3 = linear_model.LinearRegression(fit_intercept = False).fit(X3,c)
        coeff_3 = model_reg_3.coef_
        coeff_0 = 1-coeff_3[0] -coeff_3[1]
            
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "scikit model": model_reg_FL,
        "F_COP": f_COP,
        }

#%% H02D01---------------------------------------------------------------------

def model_h02d01(df):
      
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP = np.array(df["COP"])

    "Create matrix and calculations"
    X = np.column_stack([np.ones(len(SET)),SET,LExT-SET,(LExT-SET)**2,PLR])   
    model_reg = linear_model.LinearRegression().fit(X, COP)
    
    return {"scikit model": model_reg}

#%% H02D02---------------------------------------------------------------------

def model_h02d02(df):
    

    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP = np.array(df["COP"])

    "Create matrix and calculations"
    X = np.column_stack([np.ones(len(SET)),SET,LExT-SET,(LExT-SET)**2,PLR,PLR**2])
    model_reg = linear_model.LinearRegression().fit(X, COP)
    
    return {"scikit model": model_reg}

#%% H02N-----------------------------------------------------------------------

def model_h02n(df, curve, source, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
   
    if source not in ["Air","Water"]:
        raise TypeError("source must be chosen from the following list: \"Water\", \"Air\"")    
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1]
    
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([np.ones(len(SET_FL)),SET_FL,LExT_FL-SET_FL,(LExT_FL-SET_FL)**2])
    model_reg_FL = linear_model.LinearRegression().fit(X_FL, COP_FL)
    
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    X_PL = np.column_stack([np.ones(len(SET_PL)),SET_PL,LExT_PL-SET_PL, (LExT_PL-SET_PL)**2])
    COP_FL_pred = model_reg_FL.predict(X_PL)
    f_COP_model_FL = COP_PL/COP_FL_pred
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        
        def f_COP_fun(x):
            if not isinstance(x,np.ndarray):
                x = np.array(x)
            f_COP=np.ones(len(x))
            for i in range(len(x)):
                if  x[i] >= 0.25:
                    f_COP[i]=1;
                else:
                    if source =="Water":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)
                    elif source == "Air":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)*(1-0.25*(1-x[i]*4))
            return f_COP
                
        f_COP = lambda x : f_COP_fun(x)
        
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"       
        curve.sort_values("X", inplace = True)
        PLR_curve = np.array(curve["X"])
        f_COP_curve = np.array(curve["f_cop"])
        
        f_COP = lambda x : np.interp(x, PLR_curve, f_COP_curve)

    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        a=1/PLR_PL-1
        b=PLR_PL-1
        c=1/f_COP_model_FL-1
        X3=np.column_stack([a,b])
        
        model_reg_3 = linear_model.LinearRegression(fit_intercept = False).fit(X3,c)
        coeff_3 = model_reg_3.coef_
        coeff_0 = 1-coeff_3[0] -coeff_3[1]
            
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "scikit model": model_reg_FL,
        "F_COP": f_COP,
        }
#%% H03D01---------------------------------------------------------------------

def model_h03d01(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    Sfr = np.array(df["SFR [kg/s]"])
    PLR = np.array(df["PLR"])
    COP = np.array(df["COP"])

    "Create matrix and calculations"
    X = np.column_stack([np.ones(len(SET)),SET,Sfr,SET**2,PLR])
    model_reg = linear_model.LinearRegression().fit(X, COP)
    
    return {"scikit model": model_reg}

#%% H03D02---------------------------------------------------------------------

def model_h03d02(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    Sfr = np.array(df["SFR [kg/s]"])
    PLR = np.array(df["PLR"])
    COP = np.array(df["COP"])

    "Create matrix and calculations"
    X = np.column_stack([np.ones(len(SET)),SET,Sfr,SET**2,PLR, PLR**2])
    model_reg = linear_model.LinearRegression().fit(X, COP)
    
    return {"scikit model": model_reg}

#%% H03N-----------------------------------------------------------------------

def model_h03n(df, curve, source, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
    
    if source not in ["Air","Water"]:
        raise TypeError("source must be chosen from the following list: \"Water\", \"Air\"")    
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1]
    
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    Sfr_FL = np.array(df_FL["SFR [kg/s]"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([np.ones(len(SET_FL)),SET_FL, Sfr_FL,  SET_FL**2])    
    model_reg_FL = linear_model.LinearRegression().fit(X_FL, COP_FL)
    
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    Sfr_PL = np.array(df_PL["SFR [kg/s]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    X_PL = np.column_stack([np.ones(len(SET_PL)), SET_PL, Sfr_PL, SET_PL**2])   
    COP_FL_pred = model_reg_FL.predict(X_PL)
    f_COP_model_FL = COP_PL/COP_FL_pred
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"       
       
        def f_COP_fun(x):
            if not isinstance(x,np.ndarray):
                x = np.array(x)
            f_COP=np.ones(len(x))
            for i in range(len(x)):
                if  x[i] >= 0.25:
                    f_COP[i]=1;
                else:
                    if source =="Water":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)
                    elif source == "Air":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)*(1-0.25*(1-x[i]*4))
            return f_COP
                
        f_COP = lambda x : f_COP_fun(x)
        
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"     
        curve.sort_values("X", inplace = True)
        PLR_curve = np.array(curve["X"])
        f_COP_curve = np.array(curve["f_cop"])

        
        f_COP = lambda x : np.interp(x, PLR_curve, f_COP_curve)

    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"     
        a=1/PLR_PL-1
        b=PLR_PL-1
        c=1/f_COP_model_FL-1
        X3=np.column_stack([a,b])
        
        model_reg_3 = linear_model.LinearRegression(fit_intercept = False).fit(X3,c)
        coeff_3 = model_reg_3.coef_
        coeff_0 = 1-coeff_3[0] -coeff_3[1]
 
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "scikit model": model_reg_FL,
        "F_COP": f_COP,
        }

#%% H04D01---------------------------------------------------------------------

def model_h04d01(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP = np.array(df["COP"])

    "Create matrix and calculations"
    X = np.column_stack([np.ones(len(SET)), SET, LExT, LExT * SET, PLR])   
    model_reg = linear_model.LinearRegression().fit(X, COP)
    
    return {"scikit model": model_reg}

#%% H04D02---------------------------------------------------------------------

def model_h04d02(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP = np.array(df["COP"])

    "Create matrix and calculations"
    X = np.column_stack([np.ones(len(SET)), SET, LExT, LExT * SET, PLR, PLR**2])
    model_reg = linear_model.LinearRegression().fit(X,  COP)
    
    return {"scikit model": model_reg}

#%% H04N-----------------------------------------------------------------------

def model_h04n(df, curve, source, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
   
    if source not in ["Air","Water"]:
        raise TypeError("source must be chosen from the following list: \"Water\", \"Air\"")    
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1]
    
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([np.ones(len(SET_FL)), SET_FL, LExT_FL, SET_FL*LExT_FL])   
    model_reg_FL = linear_model.LinearRegression().fit(X_FL, COP_FL)
    
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    X_PL = np.column_stack([np.ones(len(SET_PL)),SET_PL, LExT_PL, SET_PL*LExT_PL])
    
    COP_FL_pred = model_reg_FL.predict(X_PL)
    
    f_COP_model_FL = COP_PL/COP_FL_pred
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        
        def f_COP_fun(x):
          if not isinstance(x,np.ndarray):
              x = np.array(x)
          f_COP=np.ones(len(x))
          for i in range(len(x)):
              if  x[i] >= 0.25:
                  f_COP[i]=1;
              else:
                  if source =="Water":
                      f_COP[i]=x[i]/(0.9*4*x[i]+0.1)
                  elif source == "Air":
                      f_COP[i]=x[i]/(0.9*4*x[i]+0.1)*(1-0.25*(1-x[i]*4))
          return f_COP
                
        f_COP = lambda x : f_COP_fun(x)
        
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"    
        curve.sort_values("X", inplace = True)
        PLR_curve = np.array(curve["X"])
        f_COP_curve = np.array(curve["f_cop"])
        
        f_COP = lambda x : np.interp(x, PLR_curve, f_COP_curve)

    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        a=1/PLR_PL-1
        b=PLR_PL-1
        c=1/f_COP_model_FL-1
        X3=np.column_stack([a,b])
        
        model_reg_3 = linear_model.LinearRegression(fit_intercept = False).fit(X3,c)
        coeff_3 = model_reg_3.coef_
        coeff_0 = 1-coeff_3[0] -coeff_3[1]
            
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "scikit model": model_reg_FL,
        "F_COP": f_COP,
        }

#%% H05D01---------------------------------------------------------------------

def model_h05d01(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    LET = np.array(df["LET [°C]"])
    PLR = np.array(df["PLR"])
    COP = np.array(df["COP"])

    "Create matrix and calculations"
    X = np.column_stack([np.ones(len(SET)), SET, LET, LET * SET, PLR])
    model_reg = linear_model.LinearRegression().fit(X, COP)
    
    return {"scikit model": model_reg}

#%% H05D02---------------------------------------------------------------------

def model_h05d02(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    LET = np.array(df["LET [°C]"])
    PLR = np.array(df["PLR"])
    COP = np.array(df["COP"])

    "Create matrix and calculations"
    X = np.column_stack([np.ones(len(SET)), SET, LET, LET * SET, PLR, PLR**2])
    model_reg = linear_model.LinearRegression().fit(X,COP)
    
    return {"scikit model": model_reg}

#%% H05N-----------------------------------------------------------------------

def model_h05n(df, curve, source, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
    
    if source not in ["Air","Water"]:
        raise TypeError("source must be chosen from the following list: \"Water\", \"Air\"")    
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1]
    
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([np.ones(len(SET_FL)), SET_FL, LET_FL, SET_FL*LET_FL])
    model_reg_FL = linear_model.LinearRegression().fit(X_FL, COP_FL)
    
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    X_PL = np.column_stack([np.ones(len(SET_PL)), SET_PL, LET_PL, SET_PL*LET_PL]) 
    COP_FL_pred = model_reg_FL.predict(X_PL)
    f_COP_model_FL = COP_PL/COP_FL_pred
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"      
        
        def f_COP_fun(x):
            if not isinstance(x,np.ndarray):
                x = np.array(x)
            f_COP=np.ones(len(x))
            for i in range(len(x)):
                if  x[i] >= 0.25:
                    f_COP[i]=1;
                else:
                    if source =="Water":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)
                    elif source == "Air":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)*(1-0.25*(1-x[i]*4))
            return f_COP
        
        f_COP = lambda x : f_COP_fun(x)
        
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"      
        curve.sort_values("X", inplace = True)
        PLR_curve = np.array(curve["X"])
        f_COP_curve = np.array(curve["f_cop"])
        
        f_COP = lambda x : np.interp(x, PLR_curve, f_COP_curve)

    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        a=1/PLR_PL-1
        b=PLR_PL-1
        c=1/f_COP_model_FL-1
        X3=np.column_stack([a,b])
        
        model_reg_3 = linear_model.LinearRegression(fit_intercept = False).fit(X3,c)
        coeff_3 = model_reg_3.coef_
        coeff_0 = 1-coeff_3[0] -coeff_3[1]
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "scikit model": model_reg_FL,
        "F_COP": f_COP,
        }

#%% H06D01---------------------------------------------------------------------

def model_h06d01(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    LET = np.array(df["LET [°C]"])
    PLR = np.array(df["PLR"])
    COP = np.array(df["COP"])
    
    "Create matrix and calculations"
    X = np.column_stack([SET, LET, PLR])
    A0 = np.zeros(6)
    
    def fun(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg = minimize(fun, A0, args = (X, COP), method = 'L-BFGS-B')    
    return {"scipy model": model_reg}

#%% H06D02---------------------------------------------------------------------

def model_h06d02(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    LET = np.array(df["LET [°C]"])
    PLR = np.array(df["PLR"])
    COP = np.array(df["COP"])
    
    "Create matrix and calculations"
    X = np.column_stack([SET, LET, PLR])

    A0 = np.zeros(7)
    
    def fun(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]* xdata[:,2]**2 + x0[6]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg = minimize(fun, A0, args = (X,  COP), method = 'L-BFGS-B')
        
    return {"scipy model": model_reg}

#%% H06N-----------------------------------------------------------------------

def model_h06n(df, curve, source, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
    
    if source not in ["Air","Water"]:
        raise TypeError("source must be chosen from the following list: \"Water\", \"Air\"")    
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1]
    
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([SET_FL, LET_FL])
    A0 = np.zeros(5)
    
    def fun_FL(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1]+ x0[4]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg_FL = minimize(fun_FL, A0, args = (X_FL, COP_FL), method = 'L-BFGS-B')
    A= model_reg_FL['x']
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    
    X_PL = np.column_stack([SET_PL, LET_PL])   
    COP_FL_pred = A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4]    
    f_COP_model_FL = COP_PL/COP_FL_pred
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"       
       
        def f_COP_fun(x):
          if not isinstance(x,np.ndarray):
              x = np.array(x)
          f_COP=np.ones(len(x))
          for i in range(len(x)):
              if  x[i] >= 0.25:
                  f_COP[i]=1;
              else:
                  if source =="Water":
                      f_COP[i]=x[i]/(0.9*4*x[i]+0.1)
                  elif source == "Air":
                      f_COP[i]=x[i]/(0.9*4*x[i]+0.1)*(1-0.25*(1-x[i]*4))
          return f_COP
      
        f_COP = lambda x : f_COP_fun(x)
        
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"       
        curve.sort_values("X", inplace = True)
        PLR_curve = np.array(curve["X"])
        f_COP_curve = np.array(curve["f_cop"])
        
        f_COP = lambda x : np.interp(x, PLR_curve, f_COP_curve)

    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        
        a=1/PLR_PL-1
        b=PLR_PL-1
        c=1/f_COP_model_FL-1
        X3=np.column_stack([a,b])
        
        model_reg_3 = linear_model.LinearRegression(fit_intercept = False).fit(X3,c)
        coeff_3 = model_reg_3.coef_
        coeff_0 = 1-coeff_3[0] -coeff_3[1]
            
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "scipy model": model_reg_FL,
        "F_COP": f_COP,
        }

#%% H07D01---------------------------------------------------------------------

def model_h07d01(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP = np.array(df["COP"])
    
    "Create matrix and calculations"
    X = np.column_stack([SET, LExT, PLR])
    A0 = np.zeros(6)
    
    def fun(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg = minimize(fun, A0, args = (X,COP), method = 'L-BFGS-B')
        
    return {"scipy model": model_reg}

#%% H07D02---------------------------------------------------------------------

def model_h07d02(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP = np.array(df["COP"])
    
    "Create matrix and calculations"
    X = np.column_stack([SET, LExT, PLR])
    A0 = np.zeros(7)
    
    def fun(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]* xdata[:,2]**2 + x0[6]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg = minimize(fun, A0, args = (X, COP), method = 'L-BFGS-B')
        
    return {"scipy model": model_reg}

#%% H07N-----------------------------------------------------------------------

def model_h07n(df, curve, source, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
    
    if source not in ["Air","Water"]:
        raise TypeError("source must be chosen from the following list: \"Water\", \"Air\"")    
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1]
    
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([SET_FL, LExT_FL])  
    A0 = np.zeros(5)
    
    def fun_FL(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1]+ x0[4]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg_FL = minimize(fun_FL, A0, args = (X_FL,COP_FL), method = 'L-BFGS-B')
    A= model_reg_FL['x']
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    
    X_PL = np.column_stack([SET_PL, LExT_PL])
    COP_FL_pred = A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4]
    f_COP_model_FL = COP_PL/COP_FL_pred
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
       
        def f_COP_fun(x):
            if not isinstance(x,np.ndarray):
                x = np.array(x)
            f_COP=np.ones(len(x))
            for i in range(len(x)):
                if  x[i] >= 0.25:
                    f_COP[i]=1;
                else:
                    if source =="Water":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)
                    elif source == "Air":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)*(1-0.25*(1-x[i]*4))
            return f_COP
                
        f_COP = lambda x : f_COP_fun(x)
        
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"      
        curve.sort_values("X", inplace = True)
        PLR_curve = np.array(curve["X"])
        f_COP_curve = np.array(curve["f_cop"])
        # f_COP = np.interp(PLR_PL, PLR_curve, f_COP_curve)
        
        f_COP = lambda x : np.interp(x, PLR_curve, f_COP_curve)

    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        
        a=1/PLR_PL-1
        b=PLR_PL-1
        c=1/f_COP_model_FL-1
        X3=np.column_stack([a,b])
        
        model_reg_3 = linear_model.LinearRegression(fit_intercept = False).fit(X3,c)
        coeff_3 = model_reg_3.coef_
        coeff_0 = 1-coeff_3[0] -coeff_3[1]
            
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "scipy model": model_reg_FL,
        "F_COP": f_COP
        }

#%% H08D01---------------------------------------------------------------------

def model_h08d01(df):
       
    "Import data as Arrays"
    SExT = np.array(df["SExT [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP = np.array(df["COP"])
    
    "Create matrix and calculations"
    X = np.column_stack([SExT, LExT, PLR])
    A0 = np.zeros(6)
    
    def fun(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg = minimize(fun, A0, args = (X,COP), method = 'L-BFGS-B')
        
    return {"scipy model": model_reg}

#%% H08D02---------------------------------------------------------------------

def model_h08d02(df):
       
    "Import data as Arrays"
    SExT = np.array(df["SExT [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP = np.array(df["COP"])
    
    "Create matrix and calculations"
    X = np.column_stack([SExT, LExT, PLR])
    A0 = np.zeros(7)
    
    def fun(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]* xdata[:,2]**2 + x0[6]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg = minimize(fun, A0, args = (X, COP), method = 'L-BFGS-B')
        
    return {"scipy model": model_reg}

#%% H08N-----------------------------------------------------------------------

def model_h08n(df, curve, source, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
    
    if source not in ["Air","Water"]:
        raise TypeError("source must be chosen from the following list: \"Water\", \"Air\"")  
        
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1]
    
    
    
    "Import data as Arrays - Full Load"
    SExT_FL = np.array(df_FL["SExT [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([SExT_FL, LExT_FL])
    A0 = np.zeros(5)
    
    def fun_FL(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1]+ x0[4]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg_FL = minimize(fun_FL, A0, args = (X_FL, COP_FL), method = 'L-BFGS-B')
    A= model_reg_FL['x']
    
    "Import data as Arrays - Part Load"
    SExT_PL = np.array(df_PL["SExT [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    
    X_PL = np.column_stack([SExT_PL, LExT_PL])
    
    COP_FL_pred = A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4]
    
    f_COP_model_FL = COP_PL/COP_FL_pred
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
       
        def f_COP_fun(x):
            if not isinstance(x,np.ndarray):
                x = np.array(x)
            f_COP=np.ones(len(x))
            for i in range(len(x)):
                if  x[i] >= 0.25:
                    f_COP[i]=1;
                else:
                    if source =="Water":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)
                    elif source == "Air":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)*(1-0.25*(1-x[i]*4))
            return f_COP
                
        f_COP = lambda x : f_COP_fun(x)
        
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"      
        curve.sort_values("X", inplace = True)
        PLR_curve = np.array(curve["X"])
        f_COP_curve = np.array(curve["f_cop"])
        
        f_COP = lambda x : np.interp(x, PLR_curve, f_COP_curve)

    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        a=1/PLR_PL-1
        b=PLR_PL-1
        c=1/f_COP_model_FL-1
        X3=np.column_stack([a,b])
        
        model_reg_3 = linear_model.LinearRegression(fit_intercept = False).fit(X3,c)
        coeff_3 = model_reg_3.coef_
        coeff_0 = 1-coeff_3[0] -coeff_3[1]
            
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "scipy model": model_reg_FL,
        "F_COP": f_COP
        }

#%% H09D01---------------------------------------------------------------------

def model_h09d01(df):
       
    "Import data as Arrays"
    SExT = np.array(df["SExT [°C]"])
    LET = np.array(df["LET [°C]"])
    PLR = np.array(df["PLR"])
    COP = np.array(df["COP"])
    
    "Create matrix and calculations"
    X = np.column_stack([SExT, LET, PLR])
    A0 = np.zeros(6)
    
    def fun(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg = minimize(fun, A0, args = (X, COP), method = 'L-BFGS-B')
        
    return {"scipy model": model_reg}

#%% H09D02---------------------------------------------------------------------

def model_h09d02(df):
       
    "Import data as Arrays"
    SExT = np.array(df["SExT [°C]"])
    LET = np.array(df["LET [°C]"])
    PLR = np.array(df["PLR"])
    COP = np.array(df["COP"])
    
    "Create matrix and calculations"
    X = np.column_stack([SExT, LET, PLR])
    A0 = np.zeros(7)
    
    def fun(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]* xdata[:,2]**2 + x0[6]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg = minimize(fun, A0, args = (X, COP), method = 'L-BFGS-B')
        
    return {"scipy model": model_reg}

#%% H09N-----------------------------------------------------------------------

def model_h09n(df, curve, source, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
     
    if source not in ["Air","Water"]:
        raise TypeError("source must be chosen from the following list: \"Water\", \"Air\"")  
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1]
   
    
    "Import data as Arrays - Full Load"
    SExT_FL = np.array(df_FL["SExT [°C]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([SExT_FL, LET_FL])  
    A0 = np.zeros(5)
    
    def fun_FL(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1]+ x0[4]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg_FL = minimize(fun_FL, A0, args = (X_FL, COP_FL), method = 'L-BFGS-B')
    A= model_reg_FL['x']
    
    "Import data as Arrays - Part Load"
    SExT_PL = np.array(df_PL["SExT [°C]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    
    X_PL = np.column_stack([SExT_PL, LET_PL])
    COP_FL_pred = A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4] 
    f_COP_model_FL = COP_PL/COP_FL_pred
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
       
        def f_COP_fun(x):
            if not isinstance(x,np.ndarray):
                x = np.array(x)
            f_COP=np.ones(len(x))
            for i in range(len(x)):
                if  x[i] >= 0.25:
                    f_COP[i]=1;
                else:
                    if source =="Water":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)
                    elif source == "Air":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)*(1-0.25*(1-x[i]*4))
            return f_COP
                
        f_COP = lambda x : f_COP_fun(x)
        
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        
        curve.sort_values("X", inplace = True)
        PLR_curve = np.array(curve["X"])
        f_COP_curve = np.array(curve["f_cop"])
        
        f_COP = lambda x : np.interp(x, PLR_curve, f_COP_curve)

    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        
        a=1/PLR_PL-1
        b=PLR_PL-1
        c=1/f_COP_model_FL-1
        X3=np.column_stack([a,b])
        
        model_reg_3 = linear_model.LinearRegression(fit_intercept = False).fit(X3,c)
        coeff_3 = model_reg_3.coef_
        coeff_0 = 1-coeff_3[0] -coeff_3[1]
        
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "scipy model": model_reg_FL,
        "F_COP": f_COP,
        }

#%% H10N-----------------------------------------------------------------------

def model_h10n(df, curve, source, design_point_T = (7,35), indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")

    if source not in ["Air","Water"]:
        raise TypeError("source must be chosen from the following list: \"Water\", \"Air\"")  
    
    "Divide between part load and full load operative points"
    df_PL= df[df['PLR']!=1]


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
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create function to calculate COP_FL_pred" 
    
    X=np.column_stack([SET_PL, LExT_PL, COP_PL])
    
    def COP_fun(x, y):
        
        SET_PL = x[:, 0]
        LExT_PL = x[:, 1]
        COP_carnot_PL=np.ones(len(SET_PL))
        COP_FL_pred=np.ones(len(SET_PL))
        
        for i in range(len(LExT_PL)):
        
            if LExT_PL[i] <= SET_PL[i]:
                COP_carnot_PL[i]=50;
            else:
                COP_carnot_PL[i] = (273+ LExT_PL[i])/(LExT_PL[i] - SET_PL[i])
        
            COP_FL_pred[i] = COP_carnot_PL[i] * eta_FL

        return COP_FL_pred
    
    COP_pred_FL= lambda x, y:  COP_fun(x, y) 
    f_COP_model_FL = COP_PL/ COP_pred_FL(X,eta_FL) 
   
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
      
        def f_COP_fun(x):
            if not isinstance(x,np.ndarray):
                x = np.array(x)
            f_COP=np.ones(len(x))
            for i in range(len(x)):
                if  x[i] >= 0.25:
                    f_COP[i]=1;
                else:
                    if source =="Water":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)
                    elif source == "Air":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)*(1-0.25*(1-x[i]*4))
            return f_COP
            
           
                
        f_COP = lambda x : f_COP_fun(x)
        
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        
        curve.sort_values("X", inplace = True)
        PLR_curve = np.array(curve["X"])
        f_COP_curve = np.array(curve["f_cop"])
        
        f_COP = lambda x : np.interp(x, PLR_curve, f_COP_curve)

    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        
        a=1/PLR_PL-1
        b=PLR_PL-1
        c=1/f_COP_model_FL-1
        X3=np.column_stack([a,b])
        
        model_reg_3 = linear_model.LinearRegression(fit_intercept = False).fit(X3,c)
        coeff_3 = model_reg_3.coef_
        coeff_0 = 1-coeff_3[0] -coeff_3[1]
            
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "Carnot efficency": eta_FL,
        "COP_pred_FL": COP_pred_FL,
        "F_COP": f_COP,
        }

#%% H11N-----------------------------------------------------------------------

def model_h11n(df, curve, source, design_point_T = (7,35), indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
    
    if source not in ["Air","Water"]:
        raise TypeError("source must be chosen from the following list: \"Water\", \"Air\"")  
    
    "Divide between part load and full load operative points"
    df_PL= df[df['PLR']!=1]
    

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
    PLR_PL = np.array(df_PL["PLR"])
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
                x = np.array(x)
            f_COP=np.ones(len(x))
            for i in range(len(x)):
                if  x[i] >= 0.25:
                    f_COP[i]=1;
                else:
                    if source =="Water":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)
                    elif source == "Air":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)*(1-0.25*(1-x[i]*4))
            return f_COP
                
        f_COP = lambda x : f_COP_fun(x)
        
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"       
        curve.sort_values("X", inplace = True)
        PLR_curve = np.array(curve["X"])
        f_COP_curve = np.array(curve["f_cop"])
        
        f_COP = lambda x : np.interp(x, PLR_curve, f_COP_curve)

    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        
        a=1/PLR_PL-1
        b=PLR_PL-1
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

def model_h12n(df, curve, source, design_point_T = (7,35), indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
    
    if source not in ["Air","Water"]:
        raise TypeError("source must be chosen from the following list: \"Water\", \"Air\"")      
    
    "Divide between part load and full load operative points"
    df_PL= df[df['PLR']!=1]
    

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
    PLR_PL = np.array(df_PL["PLR"])
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
                x = np.array(x)
            f_COP=np.ones(len(x))
            for i in range(len(x)):
                if  x[i] >= 0.25:
                    f_COP[i]=1;
                else:
                    if source =="Water":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)
                    elif source == "Air":
                        f_COP[i]=x[i]/(0.9*4*x[i]+0.1)*(1-0.25*(1-x[i]*4))
            return f_COP
                
        f_COP = lambda x : f_COP_fun(x)
        
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        
        curve.sort_values("X", inplace = True)
        PLR_curve = np.array(curve["X"])
        f_COP_curve = np.array(curve["f_cop"])
        
        f_COP = lambda x : np.interp(x, PLR_curve, f_COP_curve)

    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        
        a=1/PLR_PL-1
        b=PLR_PL-1
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
        }

#%% Load Models----------------------------------------------------------------

def load_models(df, curve, source):
    
    Model={}
    
    #%% H01D01-----------------------------------------------------------------
    
    Model['H01D01']  = model_h01d01(df)
     
    #%% H01D02-----------------------------------------------------------------
    
    Model['H01D02'] = model_h01d02(df)
    
    #%% H10N-------------------------------------------------------------------
    
    Model['H01N - mod A'] = model_h01n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    Model['H01N - mod B'] = model_h01n(df, curve, source, indirect_model = "ISO 13612-2 mod B")
    Model['H01N - mod C'] = model_h01n(df, curve, source, indirect_model = "C method")
     
    #%% H02D01-----------------------------------------------------------------
    
    Model['H02D01'] = model_h02d01(df)
    
    #%% H02D02-----------------------------------------------------------------
    
    Model['H02D02'] = model_h02d02(df)
    
    #%% H02N-------------------------------------------------------------------
    
    Model['H02N - mod A'] = model_h02n(df, curve, source, indirect_model = "ISO 13612-2 mod A" )
    Model['H02N - mod B'] = model_h02n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H02N - mod C'] = model_h02n(df, curve, source, indirect_model = "C method")
     
    #%% H03D01-----------------------------------------------------------------
    
    Model['H03D01'] = model_h03d01(df)
    
    #%% H03D02-----------------------------------------------------------------
    
    Model['H03D02'] = model_h03d02(df)
    
    #%% H03N-------------------------------------------------------------------
    
    Model['H03N - mod A'] = model_h03n(df, curve, source,  indirect_model = "ISO 13612-2 mod A")
    Model['H03N - mod B'] = model_h03n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H03N - mod C'] = model_h03n(df, curve, source, indirect_model = "C method")
    
    #%% H04D01-----------------------------------------------------------------
    
    Model['H04D01'] = model_h04d01(df)
    
    #%% H04D02-----------------------------------------------------------------
    
    Model['H04D02'] = model_h04d02(df)
    
    #%% H04N-------------------------------------------------------------------
    
    Model['H04N - mod A'] = model_h04n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    Model['H04N - mod B'] = model_h04n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H04N - mod C'] = model_h04n(df, curve, source, indirect_model = "C method")
    
    #%% H05D01-----------------------------------------------------------------
    
    Model['H05D01'] = model_h05d01(df)
    
    #%% H05D02-----------------------------------------------------------------
    
    Model['H05D02'] = model_h05d02(df)
    
    #%% H05N-------------------------------------------------------------------
    
    Model['H05N - mod A'] = model_h05n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    Model['H05N - mod B'] = model_h05n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H05N - mod C'] = model_h05n(df, curve, source, indirect_model = "C method")
    
    #%% H06D01-----------------------------------------------------------------
    
    Model['H06D01'] = model_h06d01(df)
    
    #%% H06D02-----------------------------------------------------------------
    
    Model['H06D02'] = model_h06d02(df)
    
    #%% H06N-------------------------------------------------------------------
    
    Model['H06N - mod A'] = model_h06n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    Model['H06N - mod B'] = model_h06n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H06N - mod C'] = model_h06n(df, curve, source, indirect_model = "C method")
    
    #%% H07D01-----------------------------------------------------------------
    
    Model['H07D01'] = model_h07d01(df)
    
    #%% H07D02-----------------------------------------------------------------
    
    Model['H07D02'] = model_h07d02(df)
    
    #%% H07N-------------------------------------------------------------------
    
    Model['H07N - mod A'] = model_h07n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    Model['H07N - mod B'] = model_h07n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H07N - mod C'] = model_h07n(df, curve, source, indirect_model = "C method")
    
    #%% H08D01-----------------------------------------------------------------
    
    Model['H08D01'] = model_h08d01(df)
    
    #%% H08D02-----------------------------------------------------------------
    
    Model['H08D02'] = model_h08d02(df)
    
    #%% H08N-------------------------------------------------------------------
    
    Model['H08N - mod A'] = model_h08n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    Model['H08N - mod B'] = model_h08n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H08N - mod C'] = model_h08n(df, curve, source, indirect_model = "C method")
    
    #%% H09D01-----------------------------------------------------------------
    
    Model['H09D01'] = model_h09d01(df)
    
    #%% H09D02-----------------------------------------------------------------
    
    Model['H09D02'] = model_h09d02(df)
    
    #%% H09N-------------------------------------------------------------------
    
    Model['H09N - mod A'] = model_h09n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    Model['H09N - mod B'] = model_h09n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H09N - mod C'] = model_h09n(df, curve, source, indirect_model = "C method")
    
    #%% H10N-------------------------------------------------------------------
    
    Model['H10N - mod A'] = model_h10n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    Model['H10N - mod B'] = model_h10n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H10N - mod C'] = model_h10n(df, curve, source, indirect_model = "C method")
    
    #%% H11N-------------------------------------------------------------------
    
    Model['H11N - mod A'] = model_h11n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    Model['H11N - mod B'] = model_h11n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H11N - mod C'] = model_h11n(df, curve, source, indirect_model = "C method")
    
    #%% H12N-------------------------------------------------------------------
    
    Model['H12N - mod A'] = model_h12n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    Model['H12N - mod B'] = model_h12n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H12N - mod C'] = model_h12n(df, curve, source, indirect_model = "C method")
    
    return Model

#%% Load Models----------------------------------------------------------------

def load_models2(df, curve, source):
    
    Model={}
    
    #%% H01D01-----------------------------------------------------------------
    
    #Model['H01D01']  = model_h01d01(df)
     
    #%% H01D02-----------------------------------------------------------------
    
    #Model['H01D02'] = model_h01d02(df)
    
    #%% H10N-------------------------------------------------------------------
    
    #Model['H01N - mod A'] = model_h01n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    #Model['H01N - mod B'] = model_h01n(df, curve, source, indirect_model = "ISO 13612-2 mod B")
    #Model['H01N - mod C'] = model_h01n(df, curve, source, indirect_model = "C method")
     
    #%% H02D01-----------------------------------------------------------------
    
    Model['H02D01'] = model_h02d01(df)
    
    #%% H02D02-----------------------------------------------------------------
    
    Model['H02D02'] = model_h02d02(df)
    
    #%% H02N-------------------------------------------------------------------
    
    Model['H02N - mod A'] = model_h02n(df, curve, source, indirect_model = "ISO 13612-2 mod A" )
    Model['H02N - mod B'] = model_h02n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H02N - mod C'] = model_h02n(df, curve, source, indirect_model = "C method")
     
    #%% H03D01-----------------------------------------------------------------
    
    #Model['H03D01'] = model_h03d01(df)
    
    #%% H03D02-----------------------------------------------------------------
    
    #Model['H03D02'] = model_h03d02(df)
    
    #%% H03N-------------------------------------------------------------------
    
    #Model['H03N - mod A'] = model_h03n(df, curve, source,  indirect_model = "ISO 13612-2 mod A")
    #Model['H03N - mod B'] = model_h03n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    #Model['H03N - mod C'] = model_h03n(df, curve, source, indirect_model = "C method")
    
    #%% H04D01-----------------------------------------------------------------
    
    Model['H04D01'] = model_h04d01(df)
    
    #%% H04D02-----------------------------------------------------------------
    
    Model['H04D02'] = model_h04d02(df)
    
    #%% H04N-------------------------------------------------------------------
    
    Model['H04N - mod A'] = model_h04n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    Model['H04N - mod B'] = model_h04n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H04N - mod C'] = model_h04n(df, curve, source, indirect_model = "C method")
    
    #%% H05D01-----------------------------------------------------------------
    
    Model['H05D01'] = model_h05d01(df)
    
    #%% H05D02-----------------------------------------------------------------
    
    Model['H05D02'] = model_h05d02(df)
    
    #%% H05N-------------------------------------------------------------------
    
    Model['H05N - mod A'] = model_h05n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    #Model['H05N - mod B'] = model_h05n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H05N - mod C'] = model_h05n(df, curve, source, indirect_model = "C method")
    
    #%% H06D01-----------------------------------------------------------------
    
    # Model['H06D01'] = model_h06d01(df)
    
    #%% H06D02-----------------------------------------------------------------
    
    # Model['H06D02'] = model_h06d02(df)
    

    #%% H06N-------------------------------------------------------------------
    
    Model['H06N - mod A'] = model_h06n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    # #Model['H06N - mod B'] = model_h06n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H06N - mod C'] = model_h06n(df, curve, source, indirect_model = "C method")
    
    #%% H07D01-----------------------------------------------------------------
    
    # Model['H07D01'] = model_h07d01(df)
    
    #%% H07D02-----------------------------------------------------------------
    
    # Model['H07D02'] = model_h07d02(df)
    
    #%% H07N-------------------------------------------------------------------
    
    Model['H07N - mod A'] = model_h07n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    # #Model['H07N - mod B'] = model_h07n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H07N - mod C'] = model_h07n(df, curve, source, indirect_model = "C method")
    
    #%% H08D01-----------------------------------------------------------------
    
    #Model['H08D01'] = model_h08d01(df)
    
    #%% H08D02-----------------------------------------------------------------
    
    #Model['H08D02'] = model_h08d02(df)
    
    #%% H08N-------------------------------------------------------------------
    
    #Model['H08N - mod A'] = model_h08n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    #Model['H08N - mod B'] = model_h08n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    #Model['H08N - mod C'] = model_h08n(df, curve, source, indirect_model = "C method")
    
    #%% H09D01-----------------------------------------------------------------
    
    #Model['H09D01'] = model_h09d01(df)
    
    #%% H09D02-----------------------------------------------------------------
    
    #Model['H09D02'] = model_h09d02(df)
    
    #%% H09N-------------------------------------------------------------------
    
    #Model['H09N - mod A'] = model_h09n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    #Model['H09N - mod B'] = model_h09n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    #Model['H09N - mod C'] = model_h09n(df, curve, source, indirect_model = "C method")
    
    #%% H10N-------------------------------------------------------------------
    
    Model['H10N - mod A'] = model_h10n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    #Model['H10N - mod B'] = model_h10n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H10N - mod C'] = model_h10n(df, curve, source, indirect_model = "C method")
    
    #%% H11N-------------------------------------------------------------------
    
    Model['H11N - mod A'] = model_h11n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    #Model['H11N - mod B'] = model_h11n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H11N - mod C'] = model_h11n(df, curve, source, indirect_model = "C method")
    
    #%% H12N-------------------------------------------------------------------
    
    Model['H12N - mod A'] = model_h12n(df, curve, source, indirect_model = "ISO 13612-2 mod A")
    #Model['H12N - mod B'] = model_h12n(df, curve, source, indirect_model = "ISO 13612-2 mod B")  
    Model['H12N - mod C'] = model_h12n(df, curve, source, indirect_model = "C method")
    
    return Model





















































