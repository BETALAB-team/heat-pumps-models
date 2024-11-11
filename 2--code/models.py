import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
# import seaborn as sns

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
    
    "Filter DataFrame"
    df_FL = df[df['PLF']==1]
    
    
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
        
        def f_COP(x):
            if not isinstance(x,np.ndarray):
                x = np.array([x])
            f_COP=np.ones(len(x))
            for i in range(len(x)):
                if x[i] >= 0.25:
                    f_COP[i]=1;
                else:
                    f_COP[i]=x[i]/(0.9*4*x[i]+0.1)
            
            return f_COP
        
            
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
        
        model_reg_3 = linear_model.LinearRegression().fit(X3,c)
        coeff_3 = model_reg_3.coef_
        intercept_3 = model_reg_3.intercept_
        # f_COP = np.ones(len(PLF_PL))
        # for m in range(len(PLF_PL)):
        #     f_COP[m] = PLF_PL[m]/(intercept_3+coeff_3[0]*PLF_PL[m]+coeff_3[1]*PLF_PL[m]**2)
            
        f_COP = lambda x : x/(intercept_3+coeff_3[0]*x+coeff_3[1]*x**2)
        
    return {
        "scikit model": model_reg_FL,
        "F_COP": f_COP,
        }

