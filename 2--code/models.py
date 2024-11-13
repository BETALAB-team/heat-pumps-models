import pandas as pd
import os
import numpy as np
# import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from scipy.optimize import minimize

#%% H01D01---------------------------------------------------------------------

def model_h01d01(df):
    
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    SExT = np.array(df["SExT [°C]"])
    Sfr = np.array(df["SFR [l/s]"])
    LET = np.array(df["LET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    LFR = np.array(df["LFR [kg/s]"])
    HC = np.array(df["Heat Abs EVA [kW[]"])
    PLF = np.array(df["PLF"])
    COP = np.array(df["COP"])
    
    "Create matrix and calculations"
    LExT_SET = LExT-SET
    LExT_SET_2 = (LExT-SET)**2
    cost = np.ones(len(HC))
    X = np.column_stack([cost,SET,Sfr,LExT_SET,LExT_SET_2,PLF])
    Y = COP
    
    model_reg = linear_model.LinearRegression().fit(X, Y)
    
       
    return {"scikit model": model_reg}

#%% H01D02---------------------------------------------------------------------

def model_h01d02(df):
    
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    SExT = np.array(df["SExT [°C]"])
    Sfr = np.array(df["SFR [l/s]"])
    LET = np.array(df["LET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    LFR = np.array(df["LFR [kg/s]"])
    HC = np.array(df["Heat Abs EVA [kW[]"])
    PLF = np.array(df["PLF"])
    COP = np.array(df["COP"])

    "Create matrix and calculations"
    LExT_SET = LExT-SET
    LExT_SET_2 = (LExT-SET)**2
    PLF_2 = PLF**2
    cost = np.ones(len(HC))
    X = np.column_stack([cost,SET,Sfr,LExT_SET,LExT_SET_2,PLF,PLF_2])
    Y = COP
    
    model_reg = linear_model.LinearRegression().fit(X, Y)
    
    return {"scikit model": model_reg}

#%% H01N-----------------------------------------------------------------------

def model_h01n(df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLF']==1]
    df_PL= df[df['PLF']!=1]
    
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    SExT_FL = np.array(df_FL["SExT [°C]"])
    Sfr_FL = np.array(df_FL["SFR [l/s]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    LFR_FL = np.array(df_FL["LFR [kg/s]"])
    HC_FL = np.array(df_FL["Heat Abs EVA [kW[]"])
    PLF_FL = np.array(df_FL["PLF"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    LExT_SET_FL = LExT_FL-SET_FL
    LExT_SET_2_FL = (LExT_FL-SET_FL)**2
    cost = np.ones(len(HC_FL))
    X_FL = np.column_stack([cost,SET_FL,Sfr_FL,LExT_SET_FL,LExT_SET_2_FL])
    Y_FL = COP_FL
    
    model_reg_FL = linear_model.LinearRegression().fit(X_FL, Y_FL)
    
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    SExT_PL = np.array(df_PL["SExT [°C]"])
    Sfr_PL = np.array(df_PL["SFR [l/s]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    LFR_FL = np.array(df_PL["LFR [kg/s]"])
    HC_PL = np.array(df_PL["Heat Abs EVA [kW[]"])
    PLF_PL = np.array(df_PL["PLF"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    LExT_SET_PL = LExT_PL-SET_PL
    LExT_SET_2_PL = (LExT_PL-SET_PL)**2
    cost = np.ones(len(HC_PL))
    X_PL = np.column_stack([cost,SET_PL,Sfr_PL,LExT_SET_PL,LExT_SET_2_PL])
    
    COP_FL_pred = model_reg_FL.predict(X_PL)
    
    f_COP_model_FL = COP_PL/COP_FL_pred
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"

        # f_COP=np.ones(len(PLF_PL))
 
        # for i in range(len(PLF_PL)):
        #     if PLF_PL [i] >= 0.25:
        #         f_COP[i]=1;
        #     else:
        #         f_COP[i]=PLF_PL[i]/(0.9*4*PLF_PL+0.1)
        
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
        # f_COP = np.ones(len(PLF_PL))
        # for m in range(len(PLF_PL)):
        #     f_COP[m] = PLF_PL[m]/(intercept_3+coeff_3[0]*PLF_PL[m]+coeff_3[1]*PLF_PL[m]**2)
            
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "scikit model": model_reg_FL,
        "F_COP": f_COP,
        "Debug": f_COP(PLF_PL),
        }

#%% H02D01---------------------------------------------------------------------

def model_h02d01(df):
      
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    SExT = np.array(df["SExT [°C]"])
    Sfr = np.array(df["SFR [l/s]"])
    LET = np.array(df["LET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    LFR = np.array(df["LFR [kg/s]"])
    HC = np.array(df["Heat Abs EVA [kW[]"])
    PLF = np.array(df["PLF"])
    COP = np.array(df["COP"])

    "Create matrix and calculations"
    LExT_SET = LExT-SET
    LExT_SET_2 = (LExT-SET)**2
    PLF_2 = PLF**2
    cost = np.ones(len(HC))
    X = np.column_stack([cost,SET,LExT_SET,LExT_SET_2,PLF])
    Y = COP
    
    model_reg = linear_model.LinearRegression().fit(X, Y)
    
    return {"scikit model": model_reg}

#%% H02D02---------------------------------------------------------------------

def model_h02d02(df):
    

    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    SExT = np.array(df["SExT [°C]"])
    Sfr = np.array(df["SFR [l/s]"])
    LET = np.array(df["LET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    LFR = np.array(df["LFR [kg/s]"])
    HC = np.array(df["Heat Abs EVA [kW[]"])
    PLF = np.array(df["PLF"])
    COP = np.array(df["COP"])

    "Create matrix and calculations"
    LExT_SET = LExT-SET
    LExT_SET_2 = (LExT-SET)**2
    PLF_2 = PLF**2
    cost = np.ones(len(HC))
    X = np.column_stack([cost,SET,LExT_SET,LExT_SET_2,PLF,PLF_2])
    Y = COP
    
    model_reg = linear_model.LinearRegression().fit(X, Y)
    
    return {"scikit model": model_reg}

#%% H02N-----------------------------------------------------------------------

def model_h02n(df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLF']==1]
    df_PL= df[df['PLF']!=1]
    
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    SExT_FL = np.array(df_FL["SExT [°C]"])
    Sfr_FL = np.array(df_FL["SFR [l/s]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    LFR_FL = np.array(df_FL["LFR [kg/s]"])
    HC_FL = np.array(df_FL["Heat Abs EVA [kW[]"])
    PLF_FL = np.array(df_FL["PLF"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    LExT_SET_FL = LExT_FL-SET_FL
    LExT_SET_2_FL = (LExT_FL-SET_FL)**2
    cost = np.ones(len(HC_FL))
    X_FL = np.column_stack([cost,SET_FL,LExT_SET_FL,LExT_SET_2_FL])
    Y_FL = COP_FL
    
    model_reg_FL = linear_model.LinearRegression().fit(X_FL, Y_FL)
    
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    SExT_PL = np.array(df_PL["SExT [°C]"])
    Sfr_PL = np.array(df_PL["SFR [l/s]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    LFR_FL = np.array(df_PL["LFR [kg/s]"])
    HC_PL = np.array(df_PL["Heat Abs EVA [kW[]"])
    PLF_PL = np.array(df_PL["PLF"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    LExT_SET_PL = LExT_PL-SET_PL
    LExT_SET_2_PL = (LExT_PL-SET_PL)**2
    cost = np.ones(len(HC_PL))
    X_PL = np.column_stack([cost,SET_PL,LExT_SET_PL,LExT_SET_2_PL])
    
    COP_FL_pred = model_reg_FL.predict(X_PL)
    
    f_COP_model_FL = COP_PL/COP_FL_pred
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"

        # f_COP=np.ones(len(PLF_PL))
 
        # for i in range(len(PLF_PL)):
        #     if PLF_PL [i] >= 0.25:
        #         f_COP[i]=1;
        #     else:
        #         f_COP[i]=PLF_PL[i]/(0.9*4*PLF_PL+0.1)
        
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
        # f_COP = np.ones(len(PLF_PL))
        # for m in range(len(PLF_PL)):
        #     f_COP[m] = PLF_PL[m]/(intercept_3+coeff_3[0]*PLF_PL[m]+coeff_3[1]*PLF_PL[m]**2)
            
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "scikit model": model_reg_FL,
        "F_COP": f_COP,
        "Debug": f_COP(PLF_PL),
        }
#%% H03D01---------------------------------------------------------------------

def model_h03d01(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    SExT = np.array(df["SExT [°C]"])
    Sfr = np.array(df["SFR [l/s]"])
    LET = np.array(df["LET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    LFR = np.array(df["LFR [kg/s]"])
    HC = np.array(df["Heat Abs EVA [kW[]"])
    PLF = np.array(df["PLF"])
    COP = np.array(df["COP"])

    "Create matrix and calculations"
    cost = np.ones(len(HC))
    SET_2 = SET**2
    X = np.column_stack([cost,SET,Sfr,SET_2,PLF])
    Y = COP
    
    model_reg = linear_model.LinearRegression().fit(X, Y)
    
    return {"scikit model": model_reg}

#%% H03D02---------------------------------------------------------------------

def model_h03d02(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    SExT = np.array(df["SExT [°C]"])
    Sfr = np.array(df["SFR [l/s]"])
    LET = np.array(df["LET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    LFR = np.array(df["LFR [kg/s]"])
    HC = np.array(df["Heat Abs EVA [kW[]"])
    PLF = np.array(df["PLF"])
    COP = np.array(df["COP"])

    "Create matrix and calculations"
    cost = np.ones(len(HC))
    SET_2 = SET**2
    PLF_2=PLF**2
    X = np.column_stack([cost,SET,Sfr,SET_2,PLF, PLF_2])
    Y = COP
    
    model_reg = linear_model.LinearRegression().fit(X, Y)
    
    return {"scikit model": model_reg}

#%% H03N-----------------------------------------------------------------------

def model_h03n(df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLF']==1]
    df_PL= df[df['PLF']!=1]
    
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    SExT_FL = np.array(df_FL["SExT [°C]"])
    Sfr_FL = np.array(df_FL["SFR [l/s]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    LFR_FL = np.array(df_FL["LFR [kg/s]"])
    HC_FL = np.array(df_FL["Heat Abs EVA [kW[]"])
    PLF_FL = np.array(df_FL["PLF"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    cost = np.ones(len(HC_FL))
    SET_2_FL = SET_FL**2
    X_FL = np.column_stack([cost,SET_FL, Sfr_FL, SET_2_FL])
    Y_FL = COP_FL
    
    model_reg_FL = linear_model.LinearRegression().fit(X_FL, Y_FL)
    
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    SExT_PL = np.array(df_PL["SExT [°C]"])
    Sfr_PL = np.array(df_PL["SFR [l/s]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    LFR_FL = np.array(df_PL["LFR [kg/s]"])
    HC_PL = np.array(df_PL["Heat Abs EVA [kW[]"])
    PLF_PL = np.array(df_PL["PLF"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    cost = np.ones(len(HC_PL))
    SET_2_PL = SET_PL**2
    X_PL = np.column_stack([cost, SET_PL, Sfr_PL, SET_2_PL])
    
    COP_FL_pred = model_reg_FL.predict(X_PL)
    
    f_COP_model_FL = COP_PL/COP_FL_pred
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"

        # f_COP=np.ones(len(PLF_PL))
 
        # for i in range(len(PLF_PL)):
        #     if PLF_PL [i] >= 0.25:
        #         f_COP[i]=1;
        #     else:
        #         f_COP[i]=PLF_PL[i]/(0.9*4*PLF_PL+0.1)
        
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
        # f_COP = np.ones(len(PLF_PL))
        # for m in range(len(PLF_PL)):
        #     f_COP[m] = PLF_PL[m]/(intercept_3+coeff_3[0]*PLF_PL[m]+coeff_3[1]*PLF_PL[m]**2)
            
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "scikit model": model_reg_FL,
        "F_COP": f_COP,
        "Debug": f_COP(PLF_PL),
        }

#%% H04D01---------------------------------------------------------------------

def model_h04d01(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    SExT = np.array(df["SExT [°C]"])
    Sfr = np.array(df["SFR [l/s]"])
    LET = np.array(df["LET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    LFR = np.array(df["LFR [kg/s]"])
    HC = np.array(df["Heat Abs EVA [kW[]"])
    PLF = np.array(df["PLF"])
    COP = np.array(df["COP"])

    "Create matrix and calculations"
    cost = np.ones(len(HC))
    X = np.column_stack([cost, SET, LExT, LExT * SET, PLF])
    Y = COP
    
    model_reg = linear_model.LinearRegression().fit(X, Y)
    
    return {"scikit model": model_reg}

#%% H04D02---------------------------------------------------------------------

def model_h04d02(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    SExT = np.array(df["SExT [°C]"])
    Sfr = np.array(df["SFR [l/s]"])
    LET = np.array(df["LET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    LFR = np.array(df["LFR [kg/s]"])
    HC = np.array(df["Heat Abs EVA [kW[]"])
    PLF = np.array(df["PLF"])
    COP = np.array(df["COP"])

    "Create matrix and calculations"
    cost = np.ones(len(HC))
    X = np.column_stack([cost, SET, LExT, LExT * SET, PLF, PLF**2])
    Y = COP
    
    model_reg = linear_model.LinearRegression().fit(X, Y)
    
    return {"scikit model": model_reg}

#%% H04N-----------------------------------------------------------------------

def model_h04n(df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLF']==1]
    df_PL= df[df['PLF']!=1]
    
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    SExT_FL = np.array(df_FL["SExT [°C]"])
    Sfr_FL = np.array(df_FL["SFR [l/s]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    LFR_FL = np.array(df_FL["LFR [kg/s]"])
    HC_FL = np.array(df_FL["Heat Abs EVA [kW[]"])
    PLF_FL = np.array(df_FL["PLF"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    cost = np.ones(len(HC_FL))
    X_FL = np.column_stack([cost, SET_FL, LExT_FL, SET_FL*LExT_FL])
    Y_FL = COP_FL
    
    model_reg_FL = linear_model.LinearRegression().fit(X_FL, Y_FL)
    
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    SExT_PL = np.array(df_PL["SExT [°C]"])
    Sfr_PL = np.array(df_PL["SFR [l/s]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    LFR_FL = np.array(df_PL["LFR [kg/s]"])
    HC_PL = np.array(df_PL["Heat Abs EVA [kW[]"])
    PLF_PL = np.array(df_PL["PLF"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    cost = np.ones(len(HC_PL))
    SET_2_PL = SET_PL**2
    X_PL = np.column_stack([cost,SET_PL, LExT_PL, SET_PL*LExT_PL])
    
    COP_FL_pred = model_reg_FL.predict(X_PL)
    
    f_COP_model_FL = COP_PL/COP_FL_pred
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"

        # f_COP=np.ones(len(PLF_PL))
 
        # for i in range(len(PLF_PL)):
        #     if PLF_PL [i] >= 0.25:
        #         f_COP[i]=1;
        #     else:
        #         f_COP[i]=PLF_PL[i]/(0.9*4*PLF_PL+0.1)
        
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
        # f_COP = np.ones(len(PLF_PL))
        # for m in range(len(PLF_PL)):
        #     f_COP[m] = PLF_PL[m]/(intercept_3+coeff_3[0]*PLF_PL[m]+coeff_3[1]*PLF_PL[m]**2)
            
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "scikit model": model_reg_FL,
        "F_COP": f_COP,
        "Debug": f_COP(PLF_PL),
        }

#%% H05D01---------------------------------------------------------------------

def model_h05d01(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    SExT = np.array(df["SExT [°C]"])
    Sfr = np.array(df["SFR [l/s]"])
    LET = np.array(df["LET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    LFR = np.array(df["LFR [kg/s]"])
    HC = np.array(df["Heat Abs EVA [kW[]"])
    PLF = np.array(df["PLF"])
    COP = np.array(df["COP"])

    "Create matrix and calculations"
    cost = np.ones(len(HC))
    X = np.column_stack([cost, SET, LET, LET * SET, PLF])
    Y = COP
    
    model_reg = linear_model.LinearRegression().fit(X, Y)
    
    return {"scikit model": model_reg}

#%% H05D02---------------------------------------------------------------------

def model_h05d02(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    SExT = np.array(df["SExT [°C]"])
    Sfr = np.array(df["SFR [l/s]"])
    LET = np.array(df["LET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    LFR = np.array(df["LFR [kg/s]"])
    HC = np.array(df["Heat Abs EVA [kW[]"])
    PLF = np.array(df["PLF"])
    COP = np.array(df["COP"])

    "Create matrix and calculations"
    cost = np.ones(len(HC))
    X = np.column_stack([cost, SET, LET, LET * SET, PLF, PLF**2])
    Y = COP
    
    model_reg = linear_model.LinearRegression().fit(X, Y)
    
    return {"scikit model": model_reg}

#%% H05N-----------------------------------------------------------------------

def model_h05n(df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLF']==1]
    df_PL= df[df['PLF']!=1]
    
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    SExT_FL = np.array(df_FL["SExT [°C]"])
    Sfr_FL = np.array(df_FL["SFR [l/s]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    LFR_FL = np.array(df_FL["LFR [kg/s]"])
    HC_FL = np.array(df_FL["Heat Abs EVA [kW[]"])
    PLF_FL = np.array(df_FL["PLF"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    cost = np.ones(len(HC_FL))
    X_FL = np.column_stack([cost, SET_FL, LET_FL, SET_FL*LET_FL])
    Y_FL = COP_FL
    
    model_reg_FL = linear_model.LinearRegression().fit(X_FL, Y_FL)
    
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    SExT_PL = np.array(df_PL["SExT [°C]"])
    Sfr_PL = np.array(df_PL["SFR [l/s]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    LFR_FL = np.array(df_PL["LFR [kg/s]"])
    HC_PL = np.array(df_PL["Heat Abs EVA [kW[]"])
    PLF_PL = np.array(df_PL["PLF"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    cost = np.ones(len(HC_PL))
    SET_2_PL = SET_PL**2
    X_PL = np.column_stack([cost, SET_PL, LET_PL, SET_PL*LET_PL])
    
    COP_FL_pred = model_reg_FL.predict(X_PL)
    
    f_COP_model_FL = COP_PL/COP_FL_pred
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"

        # f_COP=np.ones(len(PLF_PL))
 
        # for i in range(len(PLF_PL)):
        #     if PLF_PL [i] >= 0.25:
        #         f_COP[i]=1;
        #     else:
        #         f_COP[i]=PLF_PL[i]/(0.9*4*PLF_PL+0.1)
        
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
        # f_COP = np.ones(len(PLF_PL))
        # for m in range(len(PLF_PL)):
        #     f_COP[m] = PLF_PL[m]/(intercept_3+coeff_3[0]*PLF_PL[m]+coeff_3[1]*PLF_PL[m]**2)
            
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "scikit model": model_reg_FL,
        "F_COP": f_COP,
        "Debug": f_COP(PLF_PL),
        }

#%% H06D01---------------------------------------------------------------------

def model_h06d01(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    SExT = np.array(df["SExT [°C]"])
    Sfr = np.array(df["SFR [l/s]"])
    LET = np.array(df["LET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    LFR = np.array(df["LFR [kg/s]"])
    HC = np.array(df["Heat Abs EVA [kW[]"])
    PLF = np.array(df["PLF"])
    COP = np.array(df["COP"])
    
    "Create matrix and calculations"
    X = np.column_stack([SET, LET, PLF])
    Y = COP
    A0 = np.zeros(6)
    
    def fun(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg = minimize(fun, A0, args = (X, Y), method = 'L-BFGS-B')
        
    return {"scipy model": model_reg}

#%% H06D02---------------------------------------------------------------------

def model_h06d02(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    SExT = np.array(df["SExT [°C]"])
    Sfr = np.array(df["SFR [l/s]"])
    LET = np.array(df["LET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    LFR = np.array(df["LFR [kg/s]"])
    HC = np.array(df["Heat Abs EVA [kW[]"])
    PLF = np.array(df["PLF"])
    COP = np.array(df["COP"])
    
    "Create matrix and calculations"
    X = np.column_stack([SET, LET, PLF])
    Y = COP
    A0 = np.zeros(7)
    
    def fun(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]* xdata[:,2]**2 + x0[6]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg = minimize(fun, A0, args = (X, Y), method = 'L-BFGS-B')
        
    return {"scipy model": model_reg}

#%% H06N-----------------------------------------------------------------------

def model_h06n(df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLF']==1]
    df_PL= df[df['PLF']!=1]
    
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    SExT_FL = np.array(df_FL["SExT [°C]"])
    Sfr_FL = np.array(df_FL["SFR [l/s]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    LFR_FL = np.array(df_FL["LFR [kg/s]"])
    HC_FL = np.array(df_FL["Heat Abs EVA [kW[]"])
    PLF_FL = np.array(df_FL["PLF"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([SET_FL, LET_FL])
    Y_FL = COP_FL
    
    A0 = np.zeros(5)
    
    def fun_FL(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1]+ x0[4]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg_FL = minimize(fun_FL, A0, args = (X_FL, Y_FL), method = 'L-BFGS-B')
    A= model_reg_FL['x']
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    SExT_PL = np.array(df_PL["SExT [°C]"])
    Sfr_PL = np.array(df_PL["SFR [l/s]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    LFR_FL = np.array(df_PL["LFR [kg/s]"])
    HC_PL = np.array(df_PL["Heat Abs EVA [kW[]"])
    PLF_PL = np.array(df_PL["PLF"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    
    X_PL = np.column_stack([SET_PL, LET_PL])
    
    COP_FL_pred = A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4]
    
    f_COP_model_FL = COP_PL/COP_FL_pred
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"

        # f_COP=np.ones(len(PLF_PL))
 
        # for i in range(len(PLF_PL)):
        #     if PLF_PL [i] >= 0.25:
        #         f_COP[i]=1;
        #     else:
        #         f_COP[i]=PLF_PL[i]/(0.9*4*PLF_PL+0.1)
        
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
        # f_COP = np.ones(len(PLF_PL))
        # for m in range(len(PLF_PL)):
        #     f_COP[m] = PLF_PL[m]/(intercept_3+coeff_3[0]*PLF_PL[m]+coeff_3[1]*PLF_PL[m]**2)
            
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "scipy model": model_reg_FL,
        "F_COP": f_COP,
        "Debug": f_COP(PLF_PL),
        }

#%% H07D01---------------------------------------------------------------------

def model_h07d01(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    SExT = np.array(df["SExT [°C]"])
    Sfr = np.array(df["SFR [l/s]"])
    LET = np.array(df["LET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    LFR = np.array(df["LFR [kg/s]"])
    HC = np.array(df["Heat Abs EVA [kW[]"])
    PLF = np.array(df["PLF"])
    COP = np.array(df["COP"])
    
    "Create matrix and calculations"
    X = np.column_stack([SET, LExT, PLF])
    Y = COP
    A0 = np.zeros(6)
    
    def fun(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg = minimize(fun, A0, args = (X, Y), method = 'L-BFGS-B')
        
    return {"scipy model": model_reg}

#%% H07D02---------------------------------------------------------------------

def model_h07d02(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    SExT = np.array(df["SExT [°C]"])
    Sfr = np.array(df["SFR [l/s]"])
    LET = np.array(df["LET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    LFR = np.array(df["LFR [kg/s]"])
    HC = np.array(df["Heat Abs EVA [kW[]"])
    PLF = np.array(df["PLF"])
    COP = np.array(df["COP"])
    
    "Create matrix and calculations"
    X = np.column_stack([SET, LExT, PLF])
    Y = COP
    A0 = np.zeros(7)
    
    def fun(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]* xdata[:,2]**2 + x0[6]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg = minimize(fun, A0, args = (X, Y), method = 'L-BFGS-B')
        
    return {"scipy model": model_reg}

#%% H07N-----------------------------------------------------------------------

def model_h07n(df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLF']==1]
    df_PL= df[df['PLF']!=1]
    
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    SExT_FL = np.array(df_FL["SExT [°C]"])
    Sfr_FL = np.array(df_FL["SFR [l/s]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    LFR_FL = np.array(df_FL["LFR [kg/s]"])
    HC_FL = np.array(df_FL["Heat Abs EVA [kW[]"])
    PLF_FL = np.array(df_FL["PLF"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([SET_FL, LExT_FL])
    Y_FL = COP_FL
    
    A0 = np.zeros(5)
    
    def fun_FL(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1]+ x0[4]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg_FL = minimize(fun_FL, A0, args = (X_FL, Y_FL), method = 'L-BFGS-B')
    A= model_reg_FL['x']
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    SExT_PL = np.array(df_PL["SExT [°C]"])
    Sfr_PL = np.array(df_PL["SFR [l/s]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    LFR_FL = np.array(df_PL["LFR [kg/s]"])
    HC_PL = np.array(df_PL["Heat Abs EVA [kW[]"])
    PLF_PL = np.array(df_PL["PLF"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    
    X_PL = np.column_stack([SET_PL, LExT_PL])
    
    COP_FL_pred = A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4]
    
    f_COP_model_FL = COP_PL/COP_FL_pred
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"

        # f_COP=np.ones(len(PLF_PL))
 
        # for i in range(len(PLF_PL)):
        #     if PLF_PL [i] >= 0.25:
        #         f_COP[i]=1;
        #     else:
        #         f_COP[i]=PLF_PL[i]/(0.9*4*PLF_PL+0.1)
        
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
        # f_COP = np.ones(len(PLF_PL))
        # for m in range(len(PLF_PL)):
        #     f_COP[m] = PLF_PL[m]/(intercept_3+coeff_3[0]*PLF_PL[m]+coeff_3[1]*PLF_PL[m]**2)
            
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "scipy model": model_reg_FL,
        "F_COP": f_COP,
        "Debug": f_COP(PLF_PL),
        }

#%% H08D01---------------------------------------------------------------------

def model_h08d01(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    SExT = np.array(df["SExT [°C]"])
    Sfr = np.array(df["SFR [l/s]"])
    LET = np.array(df["LET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    LFR = np.array(df["LFR [kg/s]"])
    HC = np.array(df["Heat Abs EVA [kW[]"])
    PLF = np.array(df["PLF"])
    COP = np.array(df["COP"])
    
    "Create matrix and calculations"
    X = np.column_stack([SExT, LExT, PLF])
    Y = COP
    A0 = np.zeros(6)
    
    def fun(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg = minimize(fun, A0, args = (X, Y), method = 'L-BFGS-B')
        
    return {"scipy model": model_reg}

#%% H08D02---------------------------------------------------------------------

def model_h08d02(df):
       
    "Import data as Arrays"
    SET = np.array(df["SET [°C]"])
    SExT = np.array(df["SExT [°C]"])
    Sfr = np.array(df["SFR [l/s]"])
    LET = np.array(df["LET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    LFR = np.array(df["LFR [kg/s]"])
    HC = np.array(df["Heat Abs EVA [kW[]"])
    PLF = np.array(df["PLF"])
    COP = np.array(df["COP"])
    
    "Create matrix and calculations"
    X = np.column_stack([SExT, LExT, PLF])
    Y = COP
    A0 = np.zeros(7)
    
    def fun(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]* xdata[:,2]**2 + x0[6]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg = minimize(fun, A0, args = (X, Y), method = 'L-BFGS-B')
        
    return {"scipy model": model_reg}

#%% H08N-----------------------------------------------------------------------

def model_h08n(df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLF']==1]
    df_PL= df[df['PLF']!=1]
    
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    SExT_FL = np.array(df_FL["SExT [°C]"])
    Sfr_FL = np.array(df_FL["SFR [l/s]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    LFR_FL = np.array(df_FL["LFR [kg/s]"])
    HC_FL = np.array(df_FL["Heat Abs EVA [kW[]"])
    PLF_FL = np.array(df_FL["PLF"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([SExT_FL, LExT_FL])
    Y_FL = COP_FL
    
    A0 = np.zeros(5)
    
    def fun_FL(x0, xdata, ydata):
          
        Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1]+ x0[4]
        res = sum((ydata-Y_pred)**2)
        
        return res
    
    model_reg_FL = minimize(fun_FL, A0, args = (X_FL, Y_FL), method = 'L-BFGS-B')
    A= model_reg_FL['x']
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    SExT_PL = np.array(df_PL["SExT [°C]"])
    Sfr_PL = np.array(df_PL["SFR [l/s]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    LFR_FL = np.array(df_PL["LFR [kg/s]"])
    HC_PL = np.array(df_PL["Heat Abs EVA [kW[]"])
    PLF_PL = np.array(df_PL["PLF"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    
    X_PL = np.column_stack([SExT_PL, LExT_PL])
    
    COP_FL_pred = A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4]
    
    f_COP_model_FL = COP_PL/COP_FL_pred
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"

        # f_COP=np.ones(len(PLF_PL))
 
        # for i in range(len(PLF_PL)):
        #     if PLF_PL [i] >= 0.25:
        #         f_COP[i]=1;
        #     else:
        #         f_COP[i]=PLF_PL[i]/(0.9*4*PLF_PL+0.1)
        
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
        # f_COP = np.ones(len(PLF_PL))
        # for m in range(len(PLF_PL)):
        #     f_COP[m] = PLF_PL[m]/(intercept_3+coeff_3[0]*PLF_PL[m]+coeff_3[1]*PLF_PL[m]**2)
            
        f_COP = lambda x : x/(coeff_3[0]+coeff_0*x+coeff_3[1]*x**2)
        
    return {
        "scipy model": model_reg_FL,
        "F_COP": f_COP,
        "Debug": f_COP(PLF_PL),
        }




