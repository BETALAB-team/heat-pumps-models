import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error, root_mean_squared_error,r2_score
from models import *

#%% Test H01DO1----------------------------------------------------------------

def kpi_h01d01(Models, df, curve):
    
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
    COP_pred = Models['H01D01']['scikit model'].predict(X)
     
    
    "Evaluation of performance"
    MAE = mean_absolute_error(COP, COP_pred)
    RMSE = root_mean_squared_error(COP, COP_pred)
    r2 = r2_score(COP, COP_pred)
    
    return {"COP_pred": COP_pred,
            "MAE": MAE,
            "RMSE": RMSE,
            "r2": r2}

#%% Test H01DO1----------------------------------------------------------------

def kpi_h01d02(Models, df, curve):
    
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
    COP_pred = Models['H01D02']['scikit model'].predict(X)
    
    "Evaluation of performance"
    MAE = mean_absolute_error(COP, COP_pred)
    RMSE = root_mean_squared_error(COP, COP_pred)
    r2 = r2_score(COP, COP_pred)
    
    return {"COP_pred": COP_pred,
            "MAE": MAE,
            "RMSE": RMSE,
            "r2": r2}
#%% Test H01N----------------------------------------------------------------


def kpi_h01n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
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
    COP_FL_pred_FL = Models['H01N - mod A']['scikit model'].predict(X_FL) #COP_FL predicted starting from X_FL
    
    "Evaluation of performance-FL"
    MAE_FL = mean_absolute_error(COP_FL, COP_FL_pred_FL)
    RMSE_FL = root_mean_squared_error(COP_FL, COP_FL_pred_FL)
    r2_FL = r2_score(COP_FL, COP_FL_pred_FL)
    
    "Import data as Array - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    SExT_PL = np.array(df_PL["SExT [°C]"])
    Sfr_PL = np.array(df_PL["SFR [l/s]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    LFR_FL = np.array(df_PL["LFR [kg/s]"])
    HC_PL = np.array(df_PL["Heat Abs EVA [kW[]"])
    PLF_PL = np.array(df_PL["PLF"])
    COP_PL = np.array(df_PL["COP"])
    COP_FL = np.array(df_FL["COP"])
  
    "Create matrix and part load calculations"
    LExT_SET_PL = LExT_PL-SET_PL
    LExT_SET_2_PL = (LExT_PL-SET_PL)**2
    cost = np.ones(len(HC_PL))
    X_PL = np.column_stack([cost,SET_PL,Sfr_PL,LExT_SET_PL,LExT_SET_2_PL])
    
    COP_FL_pred = Models['H01N - mod A']['scikit model'].predict(X_PL) #COP_FL predicted starting from X_PL
    

    
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H01N - mod A']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred
    
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
       
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H01N - mod B']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H01N - mod C']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
        
    return {"COP_FL_pred": COP_FL_pred_FL,
                "MAE_FL": MAE_FL,
                "RMSE_FL": RMSE_FL,
                "r2_FL": r2_FL,
        "COP_pred": COP_pred,
                "MAE": MAE,
                "RMSE": RMSE,
                "r2": r2}

#%% Test H02DO1----------------------------------------------------------------

def kpi_h02d01(Models, df, curve):
    
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
    COP_pred = Models['H02D01']['scikit model'].predict(X)
    
    "Evaluation of performance"
    MAE = mean_absolute_error(COP, COP_pred)
    RMSE = root_mean_squared_error(COP, COP_pred)
    r2 = r2_score(COP, COP_pred)
    
    return {"COP_pred": COP_pred,
            "MAE": MAE,
            "RMSE": RMSE,
            "r2": r2}

#%% Test H02DO2----------------------------------------------------------------

def kpi_h02d02(Models, df, curve):
   
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
    COP_pred = Models['H02D02']['scikit model'].predict(X)
    
    "Evaluation of performance"
    MAE = mean_absolute_error(COP, COP_pred)
    RMSE = root_mean_squared_error(COP, COP_pred)
    r2 = r2_score(COP, COP_pred)
    
    return {"COP_pred": COP_pred,
            "MAE": MAE,
            "RMSE": RMSE,
            "r2": r2}

#%% Test H02N----------------------------------------------------------------

def kpi_h02n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
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
    COP_FL_pred_FL = Models['H02N - mod A']['scikit model'].predict(X_FL) #COP_FL predicted using X_FL
    
    "Evaluation of performance-FL"
    MAE_FL = mean_absolute_error(COP_FL, COP_FL_pred_FL)
    RMSE_FL = root_mean_squared_error(COP_FL, COP_FL_pred_FL)
    r2_FL = r2_score(COP_FL, COP_FL_pred_FL)
    
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
    COP_FL_pred = Models['H02N - mod A']['scikit model'].predict(X_PL) #COP_FL predicted using X_PL
    
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H02N - mod A']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
       
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H02N - mod B']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H02N - mod C']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
        
      
    return {"COP_FL_pred": COP_FL_pred_FL,
                "MAE_FL": MAE_FL,
                "RMSE_FL": RMSE_FL,
                "r2_FL": r2_FL,
        "COP_pred": COP_pred,
                "MAE": MAE,
                "RMSE": RMSE,
                "r2": r2}
#%% Test H03DO1----------------------------------------------------------------

def kpi_h03d01(Models, df, curve):
    
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
    COP_pred = Models['H03D01']['scikit model'].predict(X)
    
    "Evaluation of performance"
    MAE = mean_absolute_error(COP, COP_pred)
    RMSE = root_mean_squared_error(COP, COP_pred)
    r2 = r2_score(COP, COP_pred)
    
    return {"COP_pred": COP_pred,
            "MAE": MAE,
            "RMSE": RMSE,
            "r2": r2}

#%% Test H03DO2----------------------------------------------------------------

def kpi_h03d02(Models, df, curve):
   
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
    COP_pred = Models['H03D02']['scikit model'].predict(X)
    
    "Evaluation of performance"
    MAE = mean_absolute_error(COP, COP_pred)
    RMSE = root_mean_squared_error(COP, COP_pred)
    r2 = r2_score(COP, COP_pred)
    
    return {"COP_pred": COP_pred,
            "MAE": MAE,
            "RMSE": RMSE,
            "r2": r2}

#%% Test H03N----------------------------------------------------------------

def kpi_h03n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLF']==1]
    df_PL= df[df['PLF']!=1] 

  
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
    COP_FL_pred_FL = Models['H03N - mod A']['scikit model'].predict(X_FL) #COP_FL predicted using X_FL
    
    "Evaluation of performance-FL"
    MAE_FL = mean_absolute_error(COP_FL, COP_FL_pred_FL)
    RMSE_FL = root_mean_squared_error(COP_FL, COP_FL_pred_FL)
    r2_FL = r2_score(COP_FL, COP_FL_pred_FL)
    
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
    COP_FL_pred = Models['H03N - mod A']['scikit model'].predict(X_PL) #COP_FL predicted using X_PL
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H03N - mod A']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
       
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H03N - mod B']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H03N - mod C']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
        
    return {"COP_FL_pred": COP_FL_pred_FL,
                "MAE_FL": MAE_FL,
                "RMSE_FL": RMSE_FL,
                "r2_FL": r2_FL,
        "COP_pred": COP_pred,
                "MAE": MAE,
                "RMSE": RMSE,
                "r2": r2}

#%% Test H04DO1----------------------------------------------------------------

def kpi_h04d01(Models, df, curve):
    
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
    COP_pred = Models['H04D01']['scikit model'].predict(X)
    
    "Evaluation of performance"
    MAE = mean_absolute_error(COP, COP_pred)
    RMSE = root_mean_squared_error(COP, COP_pred)
    r2 = r2_score(COP, COP_pred)
    
    return {"COP_pred": COP_pred,
            "MAE": MAE,
            "RMSE": RMSE,
            "r2": r2}

#%% Test H04DO2----------------------------------------------------------------

def kpi_h04d02(Models, df, curve):
   
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
    COP_pred = Models['H04D02']['scikit model'].predict(X)
    
    "Evaluation of performance"
    MAE = mean_absolute_error(COP, COP_pred)
    RMSE = root_mean_squared_error(COP, COP_pred)
    r2 = r2_score(COP, COP_pred)
    
    return {"COP_pred": COP_pred,
            "MAE": MAE,
            "RMSE": RMSE,
            "r2": r2}

#%% Test H04N----------------------------------------------------------------

def kpi_h04n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
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
    COP_FL_pred_FL = Models['H04N - mod A']['scikit model'].predict(X_FL) #COP_FL predicted using X_FL
    
    "Evaluation of performance-FL"
    MAE_FL = mean_absolute_error(COP_FL, COP_FL_pred_FL)
    RMSE_FL = root_mean_squared_error(COP_FL, COP_FL_pred_FL)
    r2_FL = r2_score(COP_FL, COP_FL_pred_FL)
    
    
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
    COP_FL_pred = Models['H04N - mod A']['scikit model'].predict(X_PL) #COP_FL predicted using X_PL
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H04N - mod A']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
       
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H04N - mod B']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H04N - mod C']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
        
    return {"COP_FL_pred": COP_FL_pred_FL,
                "MAE_FL": MAE_FL,
                "RMSE_FL": RMSE_FL,
                "r2_FL": r2_FL,
        "COP_pred": COP_pred,
                "MAE": MAE,
                "RMSE": RMSE,
                "r2": r2}

#%% Test H05DO1----------------------------------------------------------------

def kpi_h05d01(Models, df, curve):
    
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
    COP_pred = Models['H05D01']['scikit model'].predict(X)
    
    "Evaluation of performance"
    MAE = mean_absolute_error(COP, COP_pred)
    RMSE = root_mean_squared_error(COP, COP_pred)
    r2 = r2_score(COP, COP_pred)
    
    return {"COP_pred": COP_pred,
            "MAE": MAE,
            "RMSE": RMSE,
            "r2": r2}

#%% Test H05DO2----------------------------------------------------------------

def kpi_h05d02(Models, df, curve):
   
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
    COP_pred = Models['H05D02']['scikit model'].predict(X)
    
    "Evaluation of performance"
    MAE = mean_absolute_error(COP, COP_pred)
    RMSE = root_mean_squared_error(COP, COP_pred)
    r2 = r2_score(COP, COP_pred)
    
    return {"COP_pred": COP_pred,
            "MAE": MAE,
            "RMSE": RMSE,
            "r2": r2}

#%% Test H05N----------------------------------------------------------------

def kpi_h05n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
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
    COP_FL_pred_FL = Models['H05N - mod A']['scikit model'].predict(X_FL) #COP_FL predicted using X_FL
    
    "Evaluation of performance-FL"
    MAE_FL = mean_absolute_error(COP_FL, COP_FL_pred_FL)
    RMSE_FL = root_mean_squared_error(COP_FL, COP_FL_pred_FL)
    r2_FL = r2_score(COP_FL, COP_FL_pred_FL)
    
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
    COP_FL_pred = Models['H05N - mod A']['scikit model'].predict(X_PL) #COP_FL predicted using X_PL
    
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H05N - mod A']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
       
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H05N - mod B']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H05N - mod C']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
        
    return {"COP_FL_pred": COP_FL_pred_FL,
                "MAE_FL": MAE_FL,
                "RMSE_FL": RMSE_FL,
                "r2_FL": r2_FL,
        "COP_pred": COP_pred,
                "MAE": MAE,
                "RMSE": RMSE,
                "r2": r2}

#%% Test H06DO1----------------------------------------------------------------

def kpi_h06d01(Models, df, curve):
    
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
    A = Models['H06D01']['scipy model']['x']
    COP_pred =  A[0]*np.exp(A[1]*X[:,0] + A[2]*X[:,1]) + A[3]*X[:,0]/X[:,1] + A[4] *X[:,2] +A[5]
    
    "Evaluation of performance"
    MAE = mean_absolute_error(COP, COP_pred)
    RMSE = root_mean_squared_error(COP, COP_pred)
    r2 = r2_score(COP, COP_pred)
    
    return {"COP_pred": COP_pred,
            "MAE": MAE,
            "RMSE": RMSE,
            "r2": r2}

#%% Test H06DO2----------------------------------------------------------------

def kpi_h06d02(Models, df, curve):
    
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
    A = Models['H06D02']['scipy model']['x']
    COP_pred =  A[0]*np.exp(A[1]*X[:,0] + A[2]*X[:,1]) + A[3]*X[:,0]/X[:,1] + A[4] *X[:,2] +A[5]*X[:,2]**2+A[6]
    
    
    "Evaluation of performance"
    MAE = mean_absolute_error(COP, COP_pred)
    RMSE = root_mean_squared_error(COP, COP_pred)
    r2 = r2_score(COP, COP_pred)
    
    return {"COP_pred": COP_pred,
            "MAE": MAE,
            "RMSE": RMSE,
            "r2": r2}

#%% Test H06N----------------------------------------------------------------

def kpi_h06n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
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
    A = Models['H06N - mod A']['scipy model']['x']
    COP_FL_pred_FL = A[0]*np.exp(A[1]*X_FL[:,0] + A[2]*X_FL[:,1]) + A[3]*X_FL[:,0]/X_FL[:,1] + A[4] #COP_FL predicted using X_FL
    
    "Evaluation of performance-FL"
    MAE_FL = mean_absolute_error(COP_FL, COP_FL_pred_FL)
    RMSE_FL = root_mean_squared_error(COP_FL, COP_FL_pred_FL)
    r2_FL = r2_score(COP_FL, COP_FL_pred_FL)
    
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
    COP_FL_pred = A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4] #COP_FL predicted using X_PL
    
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H06N - mod A']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
       
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H06N - mod B']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H06N - mod C']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
        
    return {"COP_FL_pred": COP_FL_pred_FL,
                "MAE_FL": MAE_FL,
                "RMSE_FL": RMSE_FL,
                "r2_FL": r2_FL,
        "COP_pred": COP_pred,
                "MAE": MAE,
                "RMSE": RMSE,
                "r2": r2}

#%% Test H07DO1----------------------------------------------------------------

def kpi_h07d01(Models, df, curve):
    
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
    A = Models['H07D01']['scipy model']['x']
    COP_pred =  A[0]*np.exp(A[1]*X[:,0] + A[2]*X[:,1]) + A[3]*X[:,0]/X[:,1] + A[4] *X[:,2] +A[5]
    
    "Evaluation of performance"
    MAE = mean_absolute_error(COP, COP_pred)
    RMSE = root_mean_squared_error(COP, COP_pred)
    r2 = r2_score(COP, COP_pred)
    
    return {"COP_pred": COP_pred,
            "MAE": MAE,
            "RMSE": RMSE,
            "r2": r2}

#%% Test H07DO2----------------------------------------------------------------

def kpi_h07d02(Models, df, curve):
    

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
    A = Models['H07D02']['scipy model']['x']
    COP_pred =  A[0]*np.exp(A[1]*X[:,0] + A[2]*X[:,1]) + A[3]*X[:,0]/X[:,1] + A[4] *X[:,2] +A[5]*X[:,2]**2+A[6]
    
    "Evaluation of performance"
    MAE = mean_absolute_error(COP, COP_pred)
    RMSE = root_mean_squared_error(COP, COP_pred)
    r2 = r2_score(COP, COP_pred)
    
    return {"COP_pred": COP_pred,
            "MAE": MAE,
            "RMSE": RMSE,
            "r2": r2}

#%% Test H07N----------------------------------------------------------------

def kpi_h07n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
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
    A = Models['H07N - mod A']['scipy model']['x']
    COP_FL_pred_FL = A[0]*np.exp(A[1]*X_FL[:,0] + A[2]*X_FL[:,1]) + A[3]*X_FL[:,0]/X_FL[:,1] + A[4] #COP_FL predicted using X_FL
    
    "Evaluation of performance-FL"
    MAE_FL = mean_absolute_error(COP_FL, COP_FL_pred_FL)
    RMSE_FL = root_mean_squared_error(COP_FL, COP_FL_pred_FL)
    r2_FL = r2_score(COP_FL, COP_FL_pred_FL)
    
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
    COP_FL_pred = A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4] #COP_FL predicted using X_PL
    
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H07N - mod A']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
       
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H07N - mod B']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H07N - mod C']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
        
    return {"COP_FL_pred": COP_FL_pred_FL,
                "MAE_FL": MAE_FL,
                "RMSE_FL": RMSE_FL,
                "r2_FL": r2_FL,
        "COP_pred": COP_pred,
                "MAE": MAE,
                "RMSE": RMSE,
                "r2": r2}

#%% Test H08DO1----------------------------------------------------------------

def kpi_h08d01(Models, df, curve):
        
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
    A = Models['H08D01']['scipy model']['x']
    COP_pred =  A[0]*np.exp(A[1]*X[:,0] + A[2]*X[:,1]) + A[3]*X[:,0]/X[:,1] + A[4] *X[:,2] +A[5]
    
    "Evaluation of performance"
    MAE = mean_absolute_error(COP, COP_pred)
    RMSE = root_mean_squared_error(COP, COP_pred)
    r2 = r2_score(COP, COP_pred)
    
    return {"COP_pred": COP_pred,
            "MAE": MAE,
            "RMSE": RMSE,
            "r2": r2}

#%% Test H08DO2----------------------------------------------------------------

def kpi_h08d02(Models, df, curve):
    
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
    A = Models['H08D02']['scipy model']['x']
    COP_pred =  A[0]*np.exp(A[1]*X[:,0] + A[2]*X[:,1]) + A[3]*X[:,0]/X[:,1] + A[4] *X[:,2] +A[5]*X[:,2]**2+A[6]
    
    "Evaluation of performance"
    MAE = mean_absolute_error(COP, COP_pred)
    RMSE = root_mean_squared_error(COP, COP_pred)
    r2 = r2_score(COP, COP_pred)
    
    return {"COP_pred": COP_pred,
            "MAE": MAE,
            "RMSE": RMSE,
            "r2": r2}

#%% Test H08N----------------------------------------------------------------

def kpi_h08n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
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
    A = Models['H08N - mod A']['scipy model']['x']
    COP_FL_pred_FL = A[0]*np.exp(A[1]*X_FL[:,0] + A[2]*X_FL[:,1]) + A[3]*X_FL[:,0]/X_FL[:,1] + A[4] #COP_FL predicted using X_FL
    
    "Evaluation of performance-FL"
    MAE_FL = mean_absolute_error(COP_FL, COP_FL_pred_FL)
    RMSE_FL = root_mean_squared_error(COP_FL, COP_FL_pred_FL)
    r2_FL = r2_score(COP_FL, COP_FL_pred_FL)
    
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
    COP_FL_pred = A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4] #COP_FL predicted using X_PL
    
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H08N - mod A']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
       
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H08N - mod B']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H08N - mod C']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
        
    return {"COP_FL_pred": COP_FL_pred_FL,
                "MAE_FL": MAE_FL,
                "RMSE_FL": RMSE_FL,
                "r2_FL": r2_FL,
        "COP_pred": COP_pred,
                "MAE": MAE,
                "RMSE": RMSE,
                "r2": r2}

#%% Test H09DO1----------------------------------------------------------------

def kpi_h09d01(Models, df, curve):
        
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
    X = np.column_stack([SExT, LET, PLF])
    A = Models['H09D01']['scipy model']['x']
    COP_pred =  A[0]*np.exp(A[1]*X[:,0] + A[2]*X[:,1]) + A[3]*X[:,0]/X[:,1] + A[4] *X[:,2] +A[5]
    
    "Evaluation of performance"
    MAE = mean_absolute_error(COP, COP_pred)
    RMSE = root_mean_squared_error(COP, COP_pred)
    r2 = r2_score(COP, COP_pred)
    
    return {"COP_pred": COP_pred,
            "MAE": MAE,
            "RMSE": RMSE,
            "r2": r2}

#%% Test H09DO2----------------------------------------------------------------

def kpi_h09d02(Models, df, curve):
    
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
    X = np.column_stack([SExT, LET, PLF])
    A = Models['H09D02']['scipy model']['x']
    COP_pred =  A[0]*np.exp(A[1]*X[:,0] + A[2]*X[:,1]) + A[3]*X[:,0]/X[:,1] + A[4] *X[:,2] +A[5]*X[:,2]**2+A[6]
    
    "Evaluation of performance"
    MAE = mean_absolute_error(COP, COP_pred)
    RMSE = root_mean_squared_error(COP, COP_pred)
    r2 = r2_score(COP, COP_pred)
    
    return {"COP_pred": COP_pred,
            "MAE": MAE,
            "RMSE": RMSE,
            "r2": r2}

#%% Test H09N----------------------------------------------------------------

def kpi_h09n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
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
    X_FL = np.column_stack([SExT_FL, LET_FL])
    A = Models['H09N - mod A']['scipy model']['x']
    COP_FL_pred_FL = A[0]*np.exp(A[1]*X_FL[:,0] + A[2]*X_FL[:,1]) + A[3]*X_FL[:,0]/X_FL[:,1] + A[4] #COP_FL predicted using X_FL
    
    "Evaluation of performance-FL"
    MAE_FL = mean_absolute_error(COP_FL, COP_FL_pred_FL)
    RMSE_FL = root_mean_squared_error(COP_FL, COP_FL_pred_FL)
    r2_FL = r2_score(COP_FL, COP_FL_pred_FL)
    
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
    
    X_PL = np.column_stack([SExT_PL, LET_PL])
    COP_FL_pred = A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4] #COP_FL predicted using X_PL
    
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H09N - mod A']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
       
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H09N - mod B']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H09N - mod C']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
        
    return {"COP_FL_pred": COP_FL_pred_FL,
                "MAE_FL": MAE_FL,
                "RMSE_FL": RMSE_FL,
                "r2_FL": r2_FL,
        "COP_pred": COP_pred,
                "MAE": MAE,
                "RMSE": RMSE,
                "r2": r2}

#%% Test H10N----------------------------------------------------------------

def kpi_h10n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
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
    X_FL=np.column_stack([SET_FL, LExT_FL, COP_FL])
    eta_FL = Models ['H10N - mod A']['Carnot efficency']
    COP_FL_pred_FL = Models ['H10N - mod A']['COP_pred_FL'](X_FL,eta_FL) #COP_FL predicted using X_FL
    
    "Evaluation of performance-FL"
    MAE_FL = mean_absolute_error(COP_FL, COP_FL_pred_FL)
    RMSE_FL = root_mean_squared_error(COP_FL, COP_FL_pred_FL)
    r2_FL = r2_score(COP_FL, COP_FL_pred_FL)
    
    
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
    X_PL =np.column_stack([SET_PL, LExT_PL, COP_PL])
    
    "Create matrix and full load calculations"
    COP_FL_pred = Models ['H10N - mod A']['COP_pred_FL'](X_PL,eta_FL) #COP_FL predicted using X_PL
        
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H10N - mod A']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
       
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H10N - mod B']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H10N - mod C']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
        
    return {"COP_FL_pred": COP_FL_pred_FL,
                "MAE_FL": MAE_FL,
                "RMSE_FL": RMSE_FL,
                "r2_FL": r2_FL,
        "COP_pred": COP_pred,
                "MAE": MAE,
                "RMSE": RMSE,
                "r2": r2}
#%% Test H11N----------------------------------------------------------------

def kpi_h11n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
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
    X_FL=np.column_stack([SET_FL, LExT_FL, COP_FL])
    eta_FL = Models ['H11N - mod A']['Carnot efficency']
    COP_FL_pred_FL = Models ['H11N - mod A']['COP_pred_FL'](X_FL,eta_FL) #COP_FL predicted using X_FL
    
    "Evaluation of performance-FL"
    MAE_FL = mean_absolute_error(COP_FL, COP_FL_pred_FL)
    RMSE_FL = root_mean_squared_error(COP_FL, COP_FL_pred_FL)
    r2_FL = r2_score(COP_FL, COP_FL_pred_FL)
    
    
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
    X_PL =np.column_stack([SET_PL, LExT_PL, COP_PL])
    
    "Create matrix and full load calculations"
    COP_FL_pred = Models ['H11N - mod A']['COP_pred_FL'](X_PL,eta_FL) #COP_FL predicted using X_PL
        
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H11N - mod A']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
       
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H11N - mod B']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H11N - mod C']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
        
    return {"COP_FL_pred": COP_FL_pred_FL,
                "MAE_FL": MAE_FL,
                "RMSE_FL": RMSE_FL,
                "r2_FL": r2_FL,
        "COP_pred": COP_pred,
                "MAE": MAE,
                "RMSE": RMSE,
                "r2": r2}

#%% Test H12N----------------------------------------------------------------

def kpi_h12n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
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
    X_FL=np.column_stack([SET_FL, LExT_FL, COP_FL])
    eta_FL = Models ['H12N - mod A']['Carnot efficency']
    COP_carnot = Models ['H12N - mod A']['COP_Carnot']
    COP_FL_pred_FL = Models ['H12N - mod A']['COP_pred_FL'](X_FL,eta_FL,COP_carnot) #COP_FL predicted using X_FL
    
    "Evaluation of performance-FL"
    MAE_FL = mean_absolute_error(COP_FL, COP_FL_pred_FL)
    RMSE_FL = root_mean_squared_error(COP_FL, COP_FL_pred_FL)
    r2_FL = r2_score(COP_FL, COP_FL_pred_FL)
    
    
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
    X_PL =np.column_stack([SET_PL, LExT_PL, COP_PL])
    
    "Create matrix and full load calculations"
    COP_FL_pred = Models ['H12N - mod A']['COP_pred_FL'](X_PL,eta_FL,COP_carnot) #COP_FL predicted using X_PL
        
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H12N - mod A']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
       
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H12N - mod B']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred 
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H12N - mod C']['F_COP'](PLF_PL)
        COP_pred = f_COP * COP_FL_pred
        
        "Evaluation of performance"
        MAE = mean_absolute_error(COP_PL, COP_pred)
        RMSE = root_mean_squared_error(COP_PL, COP_pred)
        r2 = r2_score(COP_PL, COP_pred)
        
    
        
    return {"COP_FL_pred": COP_FL_pred_FL,
                "MAE_FL": MAE_FL,
                "RMSE_FL": RMSE_FL,
                "r2_FL": r2_FL,
        "COP_pred": COP_pred,
                "MAE": MAE,
                "RMSE": RMSE,
                "r2": r2}
#%% Load Tests----------------------------------------------------------------
def load_test(df, curve):
    Models = load_models(df, curve)
    Test = {}
    
    #%% Test H01D01----------------------------------------------------------------
        
    Test['H01D01'] = kpi_h01d01(Models, df, curve)
    
    #%% Test H01D02----------------------------------------------------------------
        
    Test['H01D02'] = kpi_h01d02(Models, df, curve)
    
    #%% Test H01N------------------------------------------------------------------
        
    Test['H01N - mod A'] = kpi_h01n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    Test['H01N - mod B'] = kpi_h01n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H01N - mod C'] = kpi_h01n(Models, df, curve, indirect_model = "C method")
    
    #%% Test H02D01----------------------------------------------------------------
        
    Test['H02D01'] = kpi_h02d01(Models, df, curve)
    
    #%% Test H02D02----------------------------------------------------------------
        
    Test['H02D02'] = kpi_h02d02(Models, df, curve)
    
    #%% Test H02N------------------------------------------------------------------
        
    Test['H02N - mod A'] = kpi_h02n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    Test['H02N - mod B'] = kpi_h02n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H02N - mod C'] = kpi_h02n(Models, df, curve, indirect_model = "C method")
    
    #%% Test H03D01----------------------------------------------------------------
        
    Test['H03D01'] = kpi_h03d01(Models, df, curve)
    
    #%% Test H03D02----------------------------------------------------------------
        
    Test['H03D02'] = kpi_h03d02(Models, df, curve)
    
    #%% Test H03N------------------------------------------------------------------
        
    Test['H03N - mod A'] = kpi_h03n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    Test['H03N - mod B'] = kpi_h03n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H03N - mod C'] = kpi_h03n(Models, df, curve, indirect_model = "C method")
    
    #%% Test H04D01----------------------------------------------------------------
        
    Test['H04D01'] = kpi_h04d01(Models, df, curve)
    
    #%% Test H04D02----------------------------------------------------------------
        
    Test['H04D02'] = kpi_h04d02(Models, df, curve)
    
    #%% Test H04N------------------------------------------------------------------
        
    Test['H04N - mod A'] = kpi_h04n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    Test['H04N - mod B'] = kpi_h04n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H04N - mod C'] = kpi_h04n(Models, df, curve, indirect_model = "C method")
    
    #%% Test H05D01----------------------------------------------------------------
        
    Test['H05D01'] = kpi_h05d01(Models, df, curve)
    
    #%% Test H05D02----------------------------------------------------------------
        
    Test['H05D02'] = kpi_h05d02(Models, df, curve)
    
    #%% Test H05N------------------------------------------------------------------
        
    Test['H05N - mod A'] = kpi_h05n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    Test['H05N - mod B'] = kpi_h05n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H05N - mod C'] = kpi_h05n(Models, df, curve, indirect_model = "C method")
    
    #%% Test H06D01----------------------------------------------------------------
        
    Test['H06D01'] = kpi_h06d01(Models, df, curve)
    
    #%% Test H06D02----------------------------------------------------------------
        
    Test['H06D02'] = kpi_h06d02(Models, df, curve)
    
    #%% Test H06N------------------------------------------------------------------
        
    Test['H06N- mod A'] = kpi_h06n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    Test['H06N- mod B'] = kpi_h06n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H06N- mod C'] = kpi_h06n(Models, df, curve, indirect_model = "C method")
    
    #%% Test H07D01----------------------------------------------------------------
        
    Test['H07D01'] = kpi_h07d01(Models, df, curve)
    
    #%% Test H07D02----------------------------------------------------------------
        
    Test['H07D02'] = kpi_h07d02(Models, df, curve)
    
    #%% Test H07N------------------------------------------------------------------
        
    Test['H07N - mod A'] = kpi_h07n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    Test['H07N - mod B'] = kpi_h07n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H07N - mod C'] = kpi_h07n(Models, df, curve, indirect_model = "C method")
    
    #%% Test H08D01----------------------------------------------------------------
        
    Test['H08D01'] = kpi_h08d01(Models, df, curve)
    
    #%% Test H08D02----------------------------------------------------------------
        
    Test['H08D02'] = kpi_h08d02(Models, df, curve)
    
    #%% Test H08N------------------------------------------------------------------
        
    Test['H08N - mod A'] = kpi_h08n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    Test['H08N - mod B'] = kpi_h08n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H08N - mod C'] = kpi_h08n(Models, df, curve, indirect_model = "C method")
    
    #%% Test H09D01----------------------------------------------------------------
        
    Test['H09D01'] = kpi_h09d01(Models, df, curve)
    
    #%% Test H09D02----------------------------------------------------------------
        
    Test['H09D02'] = kpi_h09d02(Models, df, curve)
    
    #%% Test H09N------------------------------------------------------------------
        
    Test['H09N - mod A'] = kpi_h09n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    Test['H09N - mod B'] = kpi_h09n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H09N - mod C'] = kpi_h09n(Models, df, curve, indirect_model = "C method")
    
    
    #%% Test H10N------------------------------------------------------------------
        
    Test['H10N - mod A'] = kpi_h10n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    Test['H10N - mod B'] = kpi_h10n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H10N - mod C'] = kpi_h10n(Models, df, curve, indirect_model = "C method")
    
    #%% Test H11N------------------------------------------------------------------
        
    Test['H11N - mod A'] = kpi_h11n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    Test['H11N - mod B'] = kpi_h11n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H11N - mod C'] = kpi_h11n(Models, df, curve, indirect_model = "C method")
    
    #%% Test H12N------------------------------------------------------------------
        
    Test['H12N - mod A'] = kpi_h12n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    Test['H12N - mod B'] = kpi_h12n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H12N - mod C'] = kpi_h12n(Models, df, curve, indirect_model = "C method")

    return Test


    
    
    
    







































