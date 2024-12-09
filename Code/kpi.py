import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error, root_mean_squared_error,r2_score
from models import *

#%% Test H01D01----------------------------------------------------------------

def kpi_h01d01(Models, df, curve):
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    Sfr_FL = np.array(df_FL["SFR [kg/s]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    PLR_FL = np.array(df_FL["PLR"])
    COP_FL = np.array(df_FL["COP"])
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    Sfr_PL = np.array(df_PL["SFR [kg/s]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    Sfr = np.array(df["SFR [kg/s]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
    
    "Create matrix and calculations"
    X_FL= np.column_stack([np.ones(len(SET_FL)),SET_FL,Sfr_FL,LExT_FL-SET_FL,(LExT_FL-SET_FL)**2,PLR_FL])
    X_PL = np.column_stack([np.ones(len(SET_PL)),SET_PL,Sfr_PL,LExT_PL-SET_PL,(LExT_PL-SET_PL)**2,PLR_PL])
    X_TOT = np.column_stack([np.ones(len(SET)),SET,Sfr, LExT-SET,(LExT-SET)**2,PLR])
    
    COP_pred_FL = Models['H01D01']['scikit model'].predict(X_FL)
    COP_pred_PL = Models['H01D01']['scikit model'].predict(X_PL)
    COP_pred_TOT = Models['H01D01']['scikit model'].predict(X_TOT)
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","SFR [kg/s]","LExT [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"]=COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    x_variables=["SET [°C]","SFR [kg/s]","LExT [°C]","PLR"]
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"]=COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    x_variables=["SET [°C]","SFR [kg/s]","LExT [°C]","PLR"]
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"]=COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H01D02----------------------------------------------------------------

def kpi_h01d02(Models, df, curve):
      
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    Sfr_FL = np.array(df_FL["SFR [kg/s]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    PLR_FL = np.array(df_FL["PLR"])
    COP_FL = np.array(df_FL["COP"])
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    Sfr_PL = np.array(df_PL["SFR [kg/s]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    Sfr = np.array(df["SFR [kg/s]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
    
    "Create matrix and calculations"
    X_FL= np.column_stack([np.ones(len(SET_FL)),SET_FL,Sfr_FL,LExT_FL-SET_FL,(LExT_FL-SET_FL)**2,PLR_FL, PLR_FL**2])
    X_PL = np.column_stack([np.ones(len(SET_PL)),SET_PL,Sfr_PL,LExT_PL-SET_PL,(LExT_PL-SET_PL)**2,PLR_PL, PLR_PL**2])
    X_TOT = np.column_stack([np.ones(len(SET)),SET,Sfr, LExT-SET,(LExT-SET)**2,PLR, PLR**2])
    
    COP_pred_FL = Models['H01D02']['scikit model'].predict(X_FL)
    COP_pred_PL = Models['H01D02']['scikit model'].predict(X_PL)
    COP_pred_TOT = Models['H01D02']['scikit model'].predict(X_TOT)
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","SFR [kg/s]","LExT [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"]=COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    x_variables=["SET [°C]","SFR [kg/s]","LExT [°C]","PLR"]
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"]=COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    x_variables=["SET [°C]","SFR [kg/s]","LExT [°C]","PLR"]
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"]=COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H01N------------------------------------------------------------------

def kpi_h01n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 

    # FULL load calculation
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    Sfr_FL = np.array(df_FL["SFR [kg/s]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([np.ones(len(SET_FL)),SET_FL,Sfr_FL,LExT_FL-SET_FL,(LExT_FL-SET_FL)**2])
    COP_pred_FL = Models['H01N - mod A']['scikit model'].predict(X_FL) #COP_FL predicted starting from X_FL
    
    # Part load calculation
    
    "Import data as Array - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    Sfr_PL = np.array(df_PL["SFR [kg/s]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    X_PL = np.column_stack([np.ones(len(SET_PL)),SET_PL,Sfr_PL,LExT_PL-SET_PL,(LExT_PL-SET_PL)**2])
    COP_FL_pred_PL = Models['H01N - mod A']['scikit model'].predict(X_PL) #COP_FL predicted starting from X_PL
   
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H01N - mod A']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL      
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H01N - mod B']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H01N - mod C']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL
    
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    Sfr = np.array(df["SFR [kg/s]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
      
    "Create matrix and calculations-TOT"
    X_TOT = np.column_stack([np.ones(len(SET)),SET,Sfr,LExT-SET,(LExT-SET)**2])
    COP_FL_pred_TOT = Models['H01N - mod A']['scikit model'].predict(X_TOT) #COP_FL calculated for all data
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H01N - mod A']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT      
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H01N - mod B']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H01N - mod C']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT
    
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","SFR [kg/s]","LExT [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"]=COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    x_variables=["SET [°C]","SFR [kg/s]","LExT [°C]","PLR"]
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"]=COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    x_variables=["SET [°C]","SFR [kg/s]","LExT [°C]","PLR"]
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"]=COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H02D01----------------------------------------------------------------

def kpi_h02d01(Models, df, curve):
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    PLR_FL = np.array(df_FL["PLR"])
    COP_FL = np.array(df_FL["COP"])
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
       
    "Create matrix and calculations"
    X_FL = np.column_stack([np.ones(len(SET_FL)),SET_FL,LExT_FL-SET_FL,(LExT_FL-SET_FL)**2,PLR_FL])
    X_PL = np.column_stack([np.ones(len(SET_PL)),SET_PL,LExT_PL-SET_PL,(LExT_PL-SET_PL)**2,PLR_PL])
    X_TOT = np.column_stack([np.ones(len(SET)),SET,LExT-SET,(LExT-SET)**2,PLR])
    
    COP_pred_FL = Models['H02D01']['scikit model'].predict(X_FL)
    COP_pred_PL = Models['H02D01']['scikit model'].predict(X_PL)
    COP_pred_TOT = Models['H02D01']['scikit model'].predict(X_TOT)
    
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","LExT [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H02D02----------------------------------------------------------------

def kpi_h02d02(Models, df, curve):
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    PLR_FL = np.array(df_FL["PLR"])
    COP_FL = np.array(df_FL["COP"])
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
       
    "Create matrix and calculations"
    X_FL = np.column_stack([np.ones(len(SET_FL)),SET_FL,LExT_FL-SET_FL,(LExT_FL-SET_FL)**2,PLR_FL,PLR_FL**2])
    X_PL = np.column_stack([np.ones(len(SET_PL)),SET_PL,LExT_PL-SET_PL,(LExT_PL-SET_PL)**2,PLR_PL, PLR_PL**2])
    X_TOT = np.column_stack([np.ones(len(SET)),SET,LExT-SET,(LExT-SET)**2,PLR,PLR**2])
    
    COP_pred_FL = Models['H02D02']['scikit model'].predict(X_FL)
    COP_pred_PL = Models['H02D02']['scikit model'].predict(X_PL)
    COP_pred_TOT = Models['H02D02']['scikit model'].predict(X_TOT)
    
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","LExT [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H02N------------------------------------------------------------------
 
def kpi_h02n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([np.ones(len(SET_FL)),SET_FL,LExT_FL-SET_FL,(LExT_FL-SET_FL)**2])
    COP_pred_FL = Models['H02N - mod A']['scikit model'].predict(X_FL) #COP_FL predicted using X_FL
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    X_PL = np.column_stack([np.ones(len(SET_PL)),SET_PL,LExT_PL-SET_PL,(LExT_PL-SET_PL)**2])
    COP_FL_pred_PL = Models['H02N - mod A']['scikit model'].predict(X_PL) #COP_FL predicted using X_PL
    
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H02N - mod A']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL      
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H02N - mod B']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H02N - mod C']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL
        
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
      
    "Create matrix and calculations-TOT"
    X_TOT = np.column_stack([np.ones(len(SET)),SET,LExT-SET,(LExT-SET)**2])
    COP_FL_pred_TOT = Models['H02N - mod A']['scikit model'].predict(X_TOT) #COP_FL calculated for all data
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H02N - mod A']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT      
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H02N - mod B']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H02N - mod C']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT
    
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","LExT [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H03D01----------------------------------------------------------------

def kpi_h03d01(Models, df, curve):
    
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    Sfr_FL = np.array(df_FL["SFR [kg/s]"])
    PLR_FL = np.array(df_FL["PLR"])
    COP_FL = np.array(df_FL["COP"])
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    Sfr_PL = np.array(df_PL["SFR [kg/s]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    Sfr = np.array(df["SFR [kg/s]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])

    "Create matrix and calculations"
    X_FL = np.column_stack([np.ones(len(SET_FL)),SET_FL,Sfr_FL,SET_FL**2,PLR_FL])
    X_PL = np.column_stack([np.ones(len(SET_PL)),SET_PL,Sfr_PL,SET_PL**2,PLR_PL])
    X_TOT = np.column_stack([np.ones(len(SET)),SET,Sfr,SET**2,PLR])
    
    COP_pred_FL = Models['H03D01']['scikit model'].predict(X_FL)
    COP_pred_PL = Models['H03D01']['scikit model'].predict(X_PL)
    COP_pred_TOT = Models['H03D01']['scikit model'].predict(X_TOT)
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","SFR [kg/s]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H03D02----------------------------------------------------------------

def kpi_h03d02(Models, df, curve):
   
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    Sfr_FL = np.array(df_FL["SFR [kg/s]"])
    PLR_FL = np.array(df_FL["PLR"])
    COP_FL = np.array(df_FL["COP"])
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    Sfr_PL = np.array(df_PL["SFR [kg/s]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    Sfr = np.array(df["SFR [kg/s]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])

    "Create matrix and calculations"
    X_FL = np.column_stack([np.ones(len(SET_FL)),SET_FL,Sfr_FL, SET_FL**2,PLR_FL, PLR_FL**2])
    X_PL = np.column_stack([np.ones(len(SET_PL)),SET_PL,Sfr_PL, SET_PL**2,PLR_PL, PLR_PL**2])
    X_TOT = np.column_stack([np.ones(len(SET)),SET,Sfr, SET**2,PLR, PLR**2])
    
    COP_pred_FL = Models['H03D02']['scikit model'].predict(X_FL)
    COP_pred_PL = Models['H03D02']['scikit model'].predict(X_PL)
    COP_pred_TOT = Models['H03D02']['scikit model'].predict(X_TOT)
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","SFR [kg/s]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,

           "KPI_TOT": KPI_TOT}

#%% Test H03N------------------------------------------------------------------

def kpi_h03n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    Sfr_FL = np.array(df_FL["SFR [kg/s]"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([np.ones(len(SET_FL)),SET_FL,Sfr_FL,SET_FL**2])
    COP_pred_FL = Models['H03N - mod A']['scikit model'].predict(X_FL) #COP_FL predicted using X_FL
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    Sfr_PL = np.array(df_PL["SFR [kg/s]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    X_PL = np.column_stack([np.ones(len(SET_PL)),SET_PL,Sfr_PL,SET_PL**2])
    COP_FL_pred_PL = Models['H03N - mod A']['scikit model'].predict(X_PL) #COP_FL predicted using X_PL
    
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H03N - mod A']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL      
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H03N - mod B']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H03N - mod C']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL
        
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    Sfr = np.array(df["SFR [kg/s]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
      
    "Create matrix and calculations-TOT"
    X_TOT = np.column_stack([np.ones(len(SET)),SET,Sfr,SET**2])
    COP_FL_pred_TOT = Models['H03N - mod A']['scikit model'].predict(X_TOT) #COP_FL calculated for all data
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H03N - mod A']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT      
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H03N - mod B']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H03N - mod C']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT
    
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","SFR [kg/s]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}
#%% Test H04D01----------------------------------------------------------------

def kpi_h04d01(Models, df, curve):
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    PLR_FL = np.array(df_FL["PLR"])
    COP_FL = np.array(df_FL["COP"])
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])

    "Create matrix and calculations"
    X_FL = np.column_stack([np.ones(len(SET_FL)), SET_FL, LExT_FL, LExT_FL * SET_FL, PLR_FL])
    X_PL = np.column_stack([np.ones(len(SET_PL)), SET_PL, LExT_PL, LExT_PL * SET_PL, PLR_PL])
    X_TOT = np.column_stack([np.ones(len(SET)), SET, LExT, LExT * SET, PLR]) 
    
    COP_pred_FL = Models['H04D01']['scikit model'].predict(X_FL)
    COP_pred_PL = Models['H04D01']['scikit model'].predict(X_PL)
    COP_pred_TOT = Models['H04D01']['scikit model'].predict(X_TOT)
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","LExT [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H04D02----------------------------------------------------------------

def kpi_h04d02(Models, df, curve):
   
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    PLR_FL = np.array(df_FL["PLR"])
    COP_FL = np.array(df_FL["COP"])
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])

    "Create matrix and calculations"
    X_FL = np.column_stack([np.ones(len(SET_FL)), SET_FL, LExT_FL, LExT_FL * SET_FL, PLR_FL, PLR_FL**2])
    X_PL = np.column_stack([np.ones(len(SET_PL)), SET_PL, LExT_PL, LExT_PL * SET_PL, PLR_PL, PLR_PL**2])
    X_TOT = np.column_stack([np.ones(len(SET)), SET, LExT, LExT * SET, PLR, PLR**2]) 
    
    COP_pred_FL = Models['H04D02']['scikit model'].predict(X_FL)
    COP_pred_PL = Models['H04D02']['scikit model'].predict(X_PL)
    COP_pred_TOT = Models['H04D02']['scikit model'].predict(X_TOT)
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","LExT [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    
    "Evaluation of performance"
    
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H04N------------------------------------------------------------------

def kpi_h04n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([np.ones(len(SET_FL)), SET_FL, LExT_FL, SET_FL*LExT_FL])
    COP_pred_FL = Models['H04N - mod A']['scikit model'].predict(X_FL) #COP_FL predicted using X_FL
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    X_PL = np.column_stack([np.ones(len(SET_PL)), SET_PL, LExT_PL, SET_PL*LExT_PL])
    COP_FL_pred_PL = Models['H04N - mod A']['scikit model'].predict(X_PL) #COP_FL predicted using X_PL
    
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H04N - mod A']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL      
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H04N - mod B']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H04N - mod C']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL
        
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
      
    "Create matrix and calculations-TOT"
    X_TOT = np.column_stack([np.ones(len(SET)), SET, LExT, SET*LExT])
    COP_FL_pred_TOT = Models['H04N - mod A']['scikit model'].predict(X_TOT) #COP_FL calculated for all data
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H04N - mod A']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT      
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H04N - mod B']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H04N - mod C']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT
    
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","LExT [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    
    "Evaluation of performance"
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H05D01----------------------------------------------------------------

def kpi_h05d01(Models, df, curve):
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    PLR_FL = np.array(df_FL["PLR"])
    COP_FL = np.array(df_FL["COP"])
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    LET = np.array(df["LET [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])

    "Create matrix and calculations"
    X_FL = np.column_stack([np.ones(len(SET_FL)), SET_FL, LET_FL, LET_FL * SET_FL, PLR_FL])
    X_PL = np.column_stack([np.ones(len(SET_PL)), SET_PL, LET_PL, LET_PL * SET_PL, PLR_PL])
    X_TOT = np.column_stack([np.ones(len(SET)), SET, LET, LET * SET, PLR]) 
    
    COP_pred_FL = Models['H05D01']['scikit model'].predict(X_FL)
    COP_pred_PL = Models['H05D01']['scikit model'].predict(X_PL)
    COP_pred_TOT = Models['H05D01']['scikit model'].predict(X_TOT)
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","LET [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT= df_model_TOT.to_dict()
    
    "Evaluation of performance"
    
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H05D02----------------------------------------------------------------

def kpi_h05d02(Models, df, curve):
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    PLR_FL = np.array(df_FL["PLR"])
    COP_FL = np.array(df_FL["COP"])
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    LET = np.array(df["LET [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])

    "Create matrix and calculations"
    X_FL = np.column_stack([np.ones(len(SET_FL)), SET_FL, LET_FL, LET_FL * SET_FL, PLR_FL, PLR_FL**2])
    X_PL = np.column_stack([np.ones(len(SET_PL)), SET_PL, LET_PL, LET_PL * SET_PL, PLR_PL, PLR_PL**2])
    X_TOT = np.column_stack([np.ones(len(SET)), SET, LET, LET * SET, PLR, PLR**2]) 
    
    COP_pred_FL = Models['H05D02']['scikit model'].predict(X_FL)
    COP_pred_PL = Models['H05D02']['scikit model'].predict(X_PL)
    COP_pred_TOT = Models['H05D02']['scikit model'].predict(X_TOT)
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","LET [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT= df_model_TOT.to_dict()
    
    "Evaluation of performance"
    
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H05N------------------------------------------------------------------

def kpi_h05n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([np.ones(len(SET_FL)), SET_FL, LET_FL, SET_FL*LET_FL])
    COP_pred_FL = Models['H05N - mod A']['scikit model'].predict(X_FL) #COP_FL predicted using X_FL
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    X_PL = np.column_stack([np.ones(len(SET_PL)), SET_PL, LET_PL, SET_PL*LET_PL])
    COP_FL_pred_PL = Models['H05N - mod A']['scikit model'].predict(X_PL) #COP_FL predicted using X_PL
    
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H05N - mod A']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL      
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H05N - mod B']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H05N - mod C']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL
        
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    LET = np.array(df["LET [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
      
    "Create matrix and calculations-TOT"
    X_TOT = np.column_stack([np.ones(len(SET)), SET, LET, SET*LET])
    COP_FL_pred_TOT = Models['H05N - mod A']['scikit model'].predict(X_TOT) #COP_FL calculated for all data
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H05N - mod A']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT      
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H05N - mod B']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H05N - mod C']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT
    
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","LET [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT= df_model_TOT.to_dict()
    
    "Evaluation of performance"
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H06D01----------------------------------------------------------------

def kpi_h06d01(Models, df, curve):
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    PLR_FL = np.array(df_FL["PLR"])
    COP_FL = np.array(df_FL["COP"])
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    LET = np.array(df["LET [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
    
    "Create matrix and calculations"
    X_FL = np.column_stack([SET_FL, LET_FL, PLR_FL])
    X_PL = np.column_stack([SET_PL, LET_PL, PLR_PL])
    X_TOT = np.column_stack([SET, LET, PLR])
    A = Models['H06D01']['scipy model']['x']
    
    COP_pred_FL =  A[0]*np.exp(A[1]*X_FL[:,0] + A[2]*X_FL[:,1]) + A[3]*X_FL[:,0]/X_FL[:,1] + A[4] *X_FL[:,2] +A[5]
    COP_pred_PL =  A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4] *X_PL[:,2] +A[5]
    COP_pred_TOT =  A[0]*np.exp(A[1]*X_TOT[:,0] + A[2]*X_TOT[:,1]) + A[3]*X_TOT[:,0]/X_TOT[:,1] + A[4] *X_TOT[:,2] +A[5]
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","LET [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H06D02----------------------------------------------------------------

def kpi_h06d02(Models, df, curve):
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    PLR_FL = np.array(df_FL["PLR"])
    COP_FL = np.array(df_FL["COP"])
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    LET = np.array(df["LET [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
    
    "Create matrix and calculations"
    X_FL = np.column_stack([SET_FL, LET_FL, PLR_FL])
    X_PL = np.column_stack([SET_PL, LET_PL, PLR_PL])
    X_TOT = np.column_stack([SET, LET, PLR])
    A = Models['H06D02']['scipy model']['x']
    
    COP_pred_FL =  A[0]*np.exp(A[1]*X_FL[:,0] + A[2]*X_FL[:,1]) + A[3]*X_FL[:,0]/X_FL[:,1] + A[4] *X_FL[:,2] +A[5]*X_FL[:,2]**2+A[6]
    COP_pred_PL =  A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4] *X_PL[:,2] +A[5]*X_PL[:,2]**2+A[6]
    COP_pred_TOT =  A[0]*np.exp(A[1]*X_TOT[:,0] + A[2]*X_TOT[:,1]) + A[3]*X_TOT[:,0]/X_TOT[:,1] + A[4] *X_TOT[:,2] +A[5]*X_TOT[:,2]**2+A[6]
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","LET [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H06N----------------------------------------------------------------

def kpi_h06n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1]
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([SET_FL, LET_FL])
    A = Models['H06N - mod A']['scipy model']['x']
    COP_pred_FL = A[0]*np.exp(A[1]*X_FL[:,0] + A[2]*X_FL[:,1]) + A[3]*X_FL[:,0]/X_FL[:,1] + A[4] 
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    
    X_PL = np.column_stack([SET_PL, LET_PL])   
    COP_FL_pred_PL = A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4] #COP_FL predicted using X_PL
    
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H06N - mod A']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
        
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H06N - mod B']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
        
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H06N - mod C']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL
        
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    LET = np.array(df["LET [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
      
    "Create matrix and calculations-TOT"
    X_TOT = X_PL = np.column_stack([SET, LET])  
    COP_FL_pred_TOT = A[0]*np.exp(A[1]*X_TOT[:,0] + A[2]*X_TOT[:,1]) + A[3]*X_TOT[:,0]/X_TOT[:,1] + A[4] #COP_FL calculated for all data
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H06N - mod A']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT      
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H06N - mod B']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H06N - mod C']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT
    
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","LET [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}  

#%% Test H07D01----------------------------------------------------------------

def kpi_h07d01(Models, df, curve):
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    PLR_FL = np.array(df_FL["PLR"])
    COP_FL = np.array(df_FL["COP"])
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
    
    "Create matrix and calculations"
    X_FL = np.column_stack([SET_FL, LExT_FL, PLR_FL])
    X_PL = np.column_stack([SET_PL, LExT_PL, PLR_PL])
    X_TOT = np.column_stack([SET, LExT, PLR])
    A = Models['H07D01']['scipy model']['x']
    
    COP_pred_FL =  A[0]*np.exp(A[1]*X_FL[:,0] + A[2]*X_FL[:,1]) + A[3]*X_FL[:,0]/X_FL[:,1] + A[4] *X_FL[:,2] +A[5]
    COP_pred_PL =  A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4] *X_PL[:,2] +A[5]
    COP_pred_TOT =  A[0]*np.exp(A[1]*X_TOT[:,0] + A[2]*X_TOT[:,1]) + A[3]*X_TOT[:,0]/X_TOT[:,1] + A[4] *X_TOT[:,2] +A[5]
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","LExT [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H07D02----------------------------------------------------------------

def kpi_h07d02(Models, df, curve):
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    PLR_FL = np.array(df_FL["PLR"])
    COP_FL = np.array(df_FL["COP"])
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
    
    "Create matrix and calculations"
    X_FL = np.column_stack([SET_FL, LExT_FL, PLR_FL])
    X_PL = np.column_stack([SET_PL, LExT_PL, PLR_PL])
    X_TOT = np.column_stack([SET, LExT, PLR])
    A = Models['H07D02']['scipy model']['x']
    
    COP_pred_FL =  A[0]*np.exp(A[1]*X_FL[:,0] + A[2]*X_FL[:,1]) + A[3]*X_FL[:,0]/X_FL[:,1] + A[4] *X_FL[:,2] +A[5]*X_FL[:,2]**2+A[6]
    COP_pred_PL =  A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4] *X_PL[:,2] +A[5]*X_PL[:,2]**2+A[6]
    COP_pred_TOT =  A[0]*np.exp(A[1]*X_TOT[:,0] + A[2]*X_TOT[:,1]) + A[3]*X_TOT[:,0]/X_TOT[:,1] + A[4] *X_TOT[:,2] +A[5]*X_TOT[:,2]**2+A[6]
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","LExT [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H07N----------------------------------------------------------------

def kpi_h07n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1]
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([SET_FL, LExT_FL])
    A = Models['H07N - mod A']['scipy model']['x']
    COP_pred_FL = A[0]*np.exp(A[1]*X_FL[:,0] + A[2]*X_FL[:,1]) + A[3]*X_FL[:,0]/X_FL[:,1] + A[4] 
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    
    X_PL = np.column_stack([SET_PL, LExT_PL])   
    COP_FL_pred_PL = A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4] #COP_FL predicted using X_PL
    
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H07N - mod A']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
        
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H07N - mod B']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
        
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H07N - mod C']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL
        
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
      
    "Create matrix and calculations-TOT"
    X_TOT = X_PL = np.column_stack([SET, LExT])  
    COP_FL_pred_TOT = A[0]*np.exp(A[1]*X_TOT[:,0] + A[2]*X_TOT[:,1]) + A[3]*X_TOT[:,0]/X_TOT[:,1] + A[4] #COP_FL calculated for all data
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H07N - mod A']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT      
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H07N - mod B']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H07N - mod C']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT
    
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","LExT [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}  

#%% Test H08D01----------------------------------------------------------------

def kpi_h08d01(Models, df, curve):
        
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SExT_FL = np.array(df_FL["SExT [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    PLR_FL = np.array(df_FL["PLR"])
    COP_FL = np.array(df_FL["COP"])
    
    "Import data as Arrays - Part Load"
    SExT_PL = np.array(df_PL["SExT [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Import data as Arrays - TOT"
    SExT = np.array(df["SExT [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
    
    "Create matrix and calculations"
    X_FL = np.column_stack([SExT_FL, LExT_FL, PLR_FL])
    X_PL = np.column_stack([SExT_PL, LExT_PL, PLR_PL])
    X_TOT = np.column_stack([SExT, LExT, PLR])
    A = Models['H08D01']['scipy model']['x']
    
    COP_pred_FL =  A[0]*np.exp(A[1]*X_FL[:,0] + A[2]*X_FL[:,1]) + A[3]*X_FL[:,0]/X_FL[:,1] + A[4] *X_FL[:,2] +A[5]
    COP_pred_PL =  A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4] *X_PL[:,2] +A[5]
    COP_pred_TOT =  A[0]*np.exp(A[1]*X_TOT[:,0] + A[2]*X_TOT[:,1]) + A[3]*X_TOT[:,0]/X_TOT[:,1] + A[4] *X_TOT[:,2] +A[5]
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SExT [°C]","LExT [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H08D02----------------------------------------------------------------

def kpi_h08d02(Models, df, curve):
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SExT_FL = np.array(df_FL["SExT [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    PLR_FL = np.array(df_FL["PLR"])
    COP_FL = np.array(df_FL["COP"])
    
    "Import data as Arrays - Part Load"
    SExT_PL = np.array(df_PL["SExT [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Import data as Arrays - TOT"
    SExT = np.array(df["SExT [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
    
    "Create matrix and calculations"
    X_FL = np.column_stack([SExT_FL, LExT_FL, PLR_FL])
    X_PL = np.column_stack([SExT_PL, LExT_PL, PLR_PL])
    X_TOT = np.column_stack([SExT, LExT, PLR])
    A = Models['H08D02']['scipy model']['x']
    
    COP_pred_FL =  A[0]*np.exp(A[1]*X_FL[:,0] + A[2]*X_FL[:,1]) + A[3]*X_FL[:,0]/X_FL[:,1] + A[4] *X_FL[:,2] +A[5]*X_FL[:,2]**2+A[6]
    COP_pred_PL =  A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4] *X_PL[:,2] +A[5]*X_PL[:,2]**2+A[6]
    COP_pred_TOT =  A[0]*np.exp(A[1]*X_TOT[:,0] + A[2]*X_TOT[:,1]) + A[3]*X_TOT[:,0]/X_TOT[:,1] + A[4] *X_TOT[:,2] +A[5]*X_TOT[:,2]**2+A[6]
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SExT [°C]","LExT [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H08N----------------------------------------------------------------

def kpi_h08n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1]
    
    
    "Import data as Arrays - Full Load"
    SExT_FL = np.array(df_FL["SExT [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([SExT_FL, LExT_FL])
    A = Models['H08N - mod A']['scipy model']['x']
    COP_pred_FL = A[0]*np.exp(A[1]*X_FL[:,0] + A[2]*X_FL[:,1]) + A[3]*X_FL[:,0]/X_FL[:,1] + A[4] 
    
    "Import data as Arrays - Part Load"
    SExT_PL = np.array(df_PL["SExT [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    
    X_PL = np.column_stack([SExT_PL, LExT_PL])   
    COP_FL_pred_PL = A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4] #COP_FL predicted using X_PL
    
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H08N - mod A']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
        
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H08N - mod B']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
        
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H08N - mod C']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL
        
    "Import data as Arrays - TOT"
    SExT = np.array(df["SExT [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
      
    "Create matrix and calculations-TOT"
    X_TOT = X_PL = np.column_stack([SExT, LExT])  
    COP_FL_pred_TOT = A[0]*np.exp(A[1]*X_TOT[:,0] + A[2]*X_TOT[:,1]) + A[3]*X_TOT[:,0]/X_TOT[:,1] + A[4] #COP_FL calculated for all data
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H08N - mod A']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT      
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H08N - mod B']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H08N - mod C']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT
    
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SExT [°C]","LExT [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}  

#%% Test H09D01----------------------------------------------------------------

def kpi_h09d01(Models, df, curve):
        
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SExT_FL = np.array(df_FL["SExT [°C]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    PLR_FL = np.array(df_FL["PLR"])
    COP_FL = np.array(df_FL["COP"])
    
    "Import data as Arrays - Part Load"
    SExT_PL = np.array(df_PL["SExT [°C]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Import data as Arrays - TOT"
    SExT = np.array(df["SExT [°C]"])
    LET = np.array(df["LET [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
    
    "Create matrix and calculations"
    X_FL = np.column_stack([SExT_FL, LET_FL, PLR_FL])
    X_PL = np.column_stack([SExT_PL, LET_PL, PLR_PL])
    X_TOT = np.column_stack([SExT, LET, PLR])
    A = Models['H09D01']['scipy model']['x']
    
    COP_pred_FL =  A[0]*np.exp(A[1]*X_FL[:,0] + A[2]*X_FL[:,1]) + A[3]*X_FL[:,0]/X_FL[:,1] + A[4] *X_FL[:,2] +A[5]
    COP_pred_PL =  A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4] *X_PL[:,2] +A[5]
    COP_pred_TOT =  A[0]*np.exp(A[1]*X_TOT[:,0] + A[2]*X_TOT[:,1]) + A[3]*X_TOT[:,0]/X_TOT[:,1] + A[4] *X_TOT[:,2] +A[5]
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SExT [°C]","LET [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H09D02----------------------------------------------------------------

def kpi_h09d02(Models, df, curve):
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1] 
    
    "Import data as Arrays - Full Load"
    SExT_FL = np.array(df_FL["SExT [°C]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    PLR_FL = np.array(df_FL["PLR"])
    COP_FL = np.array(df_FL["COP"])
    
    "Import data as Arrays - Part Load"
    SExT_PL = np.array(df_PL["SExT [°C]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Import data as Arrays - TOT"
    SExT = np.array(df["SExT [°C]"])
    LET = np.array(df["LET [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
    
    "Create matrix and calculations"
    X_FL = np.column_stack([SExT_FL, LET_FL, PLR_FL])
    X_PL = np.column_stack([SExT_PL, LET_PL, PLR_PL])
    X_TOT = np.column_stack([SExT, LET, PLR])
    A = Models['H09D02']['scipy model']['x']
    
    COP_pred_FL =  A[0]*np.exp(A[1]*X_FL[:,0] + A[2]*X_FL[:,1]) + A[3]*X_FL[:,0]/X_FL[:,1] + A[4] *X_FL[:,2] +A[5]*X_FL[:,2]**2+A[6]
    COP_pred_PL =  A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4] *X_PL[:,2] +A[5]*X_PL[:,2]**2+A[6]
    COP_pred_TOT =  A[0]*np.exp(A[1]*X_TOT[:,0] + A[2]*X_TOT[:,1]) + A[3]*X_TOT[:,0]/X_TOT[:,1] + A[4] *X_TOT[:,2] +A[5]*X_TOT[:,2]**2+A[6]
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SExT [°C]","LET [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}

#%% Test H09N----------------------------------------------------------------

def kpi_h09n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1]
    
    
    "Import data as Arrays - Full Load"
    SExT_FL = np.array(df_FL["SExT [°C]"])
    LET_FL = np.array(df_FL["LET [°C]"])
    COP_FL = np.array(df_FL["COP"])

    "Create matrix and full load calculations"
    X_FL = np.column_stack([SExT_FL, LET_FL])
    A = Models['H09N - mod A']['scipy model']['x']
    COP_pred_FL = A[0]*np.exp(A[1]*X_FL[:,0] + A[2]*X_FL[:,1]) + A[3]*X_FL[:,0]/X_FL[:,1] + A[4] 
    
    "Import data as Arrays - Part Load"
    SExT_PL = np.array(df_PL["SExT [°C]"])
    LET_PL = np.array(df_PL["LET [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
  
    "Create matrix and part load calculations"
    
    X_PL = np.column_stack([SExT_PL, LET_PL])   
    COP_FL_pred_PL = A[0]*np.exp(A[1]*X_PL[:,0] + A[2]*X_PL[:,1]) + A[3]*X_PL[:,0]/X_PL[:,1] + A[4] #COP_FL predicted using X_PL
    
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H09N - mod A']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
        
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H09N - mod B']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
        
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H09N - mod C']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL
        
    "Import data as Arrays - TOT"
    SExT = np.array(df["SExT [°C]"])
    LET = np.array(df["LET [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
      
    "Create matrix and calculations-TOT"
    X_TOT = X_PL = np.column_stack([SExT, LET])  
    COP_FL_pred_TOT = A[0]*np.exp(A[1]*X_TOT[:,0] + A[2]*X_TOT[:,1]) + A[3]*X_TOT[:,0]/X_TOT[:,1] + A[4] #COP_FL calculated for all data
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H09N - mod A']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT      
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H09N - mod B']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H09N - mod C']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT
    
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SExT [°C]","LET [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}  

#%% Test H10N----------------------------------------------------------------

def kpi_h10n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
          
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1]
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    COP_FL = np.array(df_FL["COP"])
    
   
    
    "Create matrix and full load calculations"
    X_FL=np.column_stack([SET_FL, LExT_FL, COP_FL])
    eta_FL = Models ['H10N - mod A']['Carnot efficency']
    COP_pred_FL = Models ['H10N - mod A']['COP_pred_FL'](X_FL,eta_FL) #COP_FL predicted using X_FL
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Create matrix and full load calculations-PL"
    X_PL =np.column_stack([SET_PL, LExT_PL, COP_PL])
    COP_FL_pred_PL = Models ['H10N - mod A']['COP_pred_FL'](X_PL,eta_FL) #COP_FL predicted using X_PL
        
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H10N - mod A']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H10N - mod B']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H10N - mod C']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL
        

        
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
      
    "Create matrix and calculations-TOT"
    X_TOT =  np.column_stack([SET, LExT, COP_TOT])
    COP_FL_pred_TOT = Models ['H10N - mod A']['COP_pred_FL'](X_TOT, eta_FL) #COP_FL calculated for all data
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H10N - mod A']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT      
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H10N - mod B']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H10N - mod C']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT
    
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","LExT [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}  

#%% Test H11N----------------------------------------------------------------

def kpi_h11n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    if indirect_model not in ["ISO 13612-2 mod A", "ISO 13612-2 mod B", "C method"]:
        raise TypeError("indirect model must be chosen from the following list: \"ISO 13612-2 mod A\", \"ISO 13612-2 mod B\", \"C method\"")
        
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1]
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    COP_FL = np.array(df_FL["COP"])
    
   
    
    "Create matrix and full load calculations"
    X_FL=np.column_stack([SET_FL, LExT_FL, COP_FL])
    eta_FL = Models ['H11N - mod A']['Carnot efficency']
    COP_pred_FL = Models ['H11N - mod A']['COP_pred_FL'](X_FL,eta_FL) #COP_FL predicted using X_FL
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Create matrix and full load calculations-PL"
    X_PL =np.column_stack([SET_PL, LExT_PL, COP_PL])
    COP_FL_pred_PL = Models ['H11N - mod A']['COP_pred_FL'](X_PL,eta_FL) #COP_FL predicted using X_PL
        
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H11N - mod A']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H11N - mod B']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H11N - mod C']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL
        

        
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
      
    "Create matrix and calculations-TOT"
    X_TOT =  np.column_stack([SET, LExT, COP_TOT])
    COP_FL_pred_TOT = Models ['H11N - mod A']['COP_pred_FL'](X_TOT, eta_FL) #COP_FL calculated for all data
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H11N - mod A']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT      
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H11N - mod B']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H11N - mod C']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT
    
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","LExT [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}  

#%% Test H12N------------------------------------------------------------------

def kpi_h12n(Models, df, curve, indirect_model = "ISO 13612-2 mod A"):
    
    "Divide between part load and full load operative points"
    df_FL = df[df['PLR']==1]
    df_PL= df[df['PLR']!=1]
    
    
    "Import data as Arrays - Full Load"
    SET_FL = np.array(df_FL["SET [°C]"])
    LExT_FL = np.array(df_FL["LExT [°C]"])
    COP_FL = np.array(df_FL["COP"])
    
    "Create matrix and full load calculations"
    eta_FL = Models ['H12N - mod A']['Carnot efficency']
    X_FL=np.column_stack([SET_FL, LExT_FL, COP_FL])
    COP_carnot = Models ['H12N - mod A']['COP_Carnot']
    COP_pred_FL = Models ['H12N - mod A']['COP_pred_FL'](X_FL,eta_FL,COP_carnot)
    
    "Import data as Arrays - Part Load"
    SET_PL = np.array(df_PL["SET [°C]"])
    LExT_PL = np.array(df_PL["LExT [°C]"])
    PLR_PL = np.array(df_PL["PLR"])
    COP_PL = np.array(df_PL["COP"])
    
    "Create matrix and full load calculations-PL"
    X_PL =np.column_stack([SET_PL, LExT_PL, COP_PL])
    COP_FL_pred_PL = Models ['H12N - mod A']['COP_pred_FL'](X_PL,eta_FL,COP_carnot) #COP_FL predicted using X_PL
        
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H12N - mod A']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H12N - mod B']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H12N - mod C']['F_COP'](PLR_PL)
        COP_pred_PL = f_COP * COP_FL_pred_PL
         
    "Import data as Arrays - TOT"
    SET = np.array(df["SET [°C]"])
    LExT = np.array(df["LExT [°C]"])
    PLR = np.array(df["PLR"])
    COP_TOT = np.array(df["COP"])
      
    "Create matrix and calculations-TOT"
    X_TOT =  np.column_stack([SET, LExT, COP_TOT])
    COP_FL_pred_TOT = Models ['H12N - mod A']['COP_pred_FL'](X_TOT, eta_FL,COP_carnot) #COP_FL calculated for all data
    
    if indirect_model == "ISO 13612-2 mod A":
        
        "Method 1: f_cop by linear regression"
        f_COP =  Models['H12N - mod A']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT      
            
    elif indirect_model == "ISO 13612-2 mod B":
        
        "Method 2: f_cop derived by curves"
        f_COP =  Models['H12N - mod B']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT 
    
    elif indirect_model == "C method":
        
        "Method 3: f_cop calculated"
        f_COP =  Models['H12N - mod C']['F_COP'](PLR)
        COP_pred_TOT = f_COP * COP_FL_pred_TOT
    
    
    "Create output table"
    df_model_FL=df_FL.copy()
    x_variables=["SET [°C]","LExT [°C]","PLR"]
    df_model_FL = df_model_FL[x_variables]
    df_model_FL["COP_pred"] = COP_pred_FL
    df_model_FL = df_model_FL.to_dict()
    
    df_model_PL=df_PL.copy()
    df_model_PL = df_model_PL[x_variables]
    df_model_PL["COP_pred"] = COP_pred_PL
    df_model_PL = df_model_PL.to_dict()
    
    df_model_TOT=df.copy()
    df_model_TOT = df_model_TOT[x_variables]
    df_model_TOT["COP_pred"] = COP_pred_TOT
    df_model_TOT = df_model_TOT.to_dict()
    
    "Evaluation of performance"
    KPI_FL = {}
    KPI_PL = {}
    KPI_TOT = {}
    
    KPI_FL["MAE_FL"]  = mean_absolute_error(COP_FL, COP_pred_FL)
    KPI_FL["RMSE_FL"]  = root_mean_squared_error(COP_FL, COP_pred_FL)
    KPI_FL["r2_FL"] = r2_score(COP_FL, COP_pred_FL)
    
    KPI_PL["MAE_PL"]= mean_absolute_error(COP_PL, COP_pred_PL)
    KPI_PL["RMSE_PL"] = root_mean_squared_error(COP_PL, COP_pred_PL)
    KPI_PL["r2_PL"] = r2_score(COP_PL, COP_pred_PL)
    
    KPI_TOT["MAE_TOT"] = mean_absolute_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["RMSE_TOT"] = root_mean_squared_error(COP_TOT, COP_pred_TOT)
    KPI_TOT["r2_TOT"] = r2_score(COP_TOT, COP_pred_TOT)
    
    
    return {"df_FL":df_model_FL,
            "df_PL":df_model_PL,
            "df_tot":df_model_TOT,
           "KPI_FL": KPI_FL,
           "KPI_PL": KPI_PL,
           "KPI_TOT": KPI_TOT}  


#%% Load Tests-----------------------------------------------------------------

def load_test(Models, df, curve, Name):
    
    Test = {}
    import json
    
    "Create Folder"
    if not os.path.exists(os.path.join('..',"Results",f"{Name}")):
        os.mkdir(os.path.join('..',"Results",f"{Name}"))
    else:
        pass
    
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
    
#%% Save as Jason file --------------------------------------------------------
    
    with open(os.path.join('..',"Results",f"{Name}",f'{Name}_KPI.json'), 'w') as f:
     json.dump(Test, f)
    
    return Test

#%% Graph_COP_pred-------------------------------------------------------------

def load_graph(KPI, df, Name):
    
    "Set plot theme"
    sns.set_theme(rc={'figure.figsize':(19,9.5)})
    plt.tight_layout()
    
    
    for g in KPI.keys():
        COP = np.array(df["COP"])
        COP_pred = KPI[g]["df_tot"]["COP_pred"]
        
        plt.plot(COP,COP_pred.values(),"o", color = "orange", markeredgecolor = "black", label = "COP_pred")
        plt.plot([0, 10], [0, 10], "k--", label = "Bisector")
       
        plt.plot([0, 10], [0, 12], "k--", label = "Error +20%")
        plt.text( 6, 4.5, "+20%")
        
        plt.plot([0, 10], [0, 8], "k--", label = "Error -20%")
        plt.text( 6, 7.7, "-20%")

        plt.xlabel("COP")
        plt.xlim(0,10)
        plt.ylim(0,10)
        plt.ylabel('$COP_{pred}$')
        plt.legend()
        plt.title(f"{g}")
        sns.set_theme(rc={'figure.figsize':(19,9.5)})
        plt.tight_layout()
        plt.savefig(os.path.join('..',"Results",f"{Name}", f"{Name}_Plot_{g}.png")) #To modify to svg when defined 
        plt.close()

    
        Direct_Models = {}
        Indirect_Models = {}
        Linear_Dir = {}
        Linear_Ind = {}
        Exponential_Dir = {}
        Exponential_Ind = {}
        Carnot = {}
        
        " Divide the results in different dictionaries"
        for g in KPI.keys():
            list(g)
            if 'D' is g[3]:
                Direct_Models[g] = KPI[g]
                for m in Direct_Models.keys():
                    list(m)
                    if int(m[2]) < 6:
                        Linear_Dir[m] = Direct_Models[m]
                    else:
                        Exponential_Dir[m] = Direct_Models[m]
            else:
                Indirect_Models[g] = KPI[g]
                for m in Indirect_Models.keys():
                    list(m)
                    if int(m[1]+m[2]) <6:
                        Linear_Ind[m] = Indirect_Models[m]
                    elif int(m[1]+m[2]) >= 6 and int(m[1]+m[2]) <= 9:
                        Exponential_Ind[m] = Indirect_Models[m]
                    elif int(m[1]+m[2]) >9 :
                        Carnot[m] = Indirect_Models[m]
        
        "Extract the KPI parameters for FL, PL and TOT "
        r2_LD_TOT = []
        r2_LI_TOT = []
        r2_ED_TOT = []
        r2_EI_TOT = []
        r2_C_TOT = []
        
        r2_LD_FL = []
        r2_LI_FL = []
        r2_ED_FL = []
        r2_EI_FL = []
        r2_C_FL = []
        
        r2_LD_PL = []
        r2_LI_PL = []
        r2_ED_PL = []
        r2_EI_PL = []
        r2_C_PL = []
        
        for g in Linear_Dir.keys():
            r2_LD_TOT.append(Linear_Dir[f'{g}']['KPI_TOT']['r2_TOT'])
            r2_LD_FL.append(Linear_Dir[f'{g}']['KPI_FL']['r2_FL'])
            r2_LD_PL.append(Linear_Dir[f'{g}']['KPI_PL']['r2_PL'])
        for g in Linear_Ind.keys():
            r2_LI_TOT.append(Linear_Ind[f'{g}']['KPI_TOT']['r2_TOT'])
            r2_LI_FL.append(Linear_Ind[f'{g}']['KPI_FL']['r2_FL'])
            r2_LI_PL.append(Linear_Ind[f'{g}']['KPI_PL']['r2_PL'])
        for g in Exponential_Dir.keys():
            r2_ED_TOT.append(Exponential_Dir[f'{g}']['KPI_TOT']['r2_TOT'])
            r2_ED_FL.append(Exponential_Dir[f'{g}']['KPI_FL']['r2_FL'])
            r2_ED_PL.append(Exponential_Dir[f'{g}']['KPI_PL']['r2_PL'])
        for g in Exponential_Ind.keys():
            r2_EI_TOT.append(Exponential_Ind[f'{g}']['KPI_TOT']['r2_TOT']) 
            r2_EI_FL.append(Exponential_Ind[f'{g}']['KPI_FL']['r2_FL']) 
            r2_EI_PL.append(Exponential_Ind[f'{g}']['KPI_PL']['r2_PL']) 
        for g in Carnot.keys():
            r2_C_TOT.append(Carnot[f'{g}']['KPI_TOT']['r2_TOT'])
            r2_C_FL.append(Carnot[f'{g}']['KPI_FL']['r2_FL'])
            r2_C_PL.append(Carnot[f'{g}']['KPI_PL']['r2_PL'])
        
        MAE_LD_TOT = []
        MAE_LI_TOT = []
        MAE_ED_TOT = []
        MAE_EI_TOT = []
        MAE_C_TOT = []
        
        MAE_LD_FL = []
        MAE_LI_FL = []
        MAE_ED_FL = []
        MAE_EI_FL = []
        MAE_C_FL = []
        
        MAE_LD_PL = []
        MAE_LI_PL = []
        MAE_ED_PL = []
        MAE_EI_PL = []
        MAE_C_PL = []
        
        for g in Linear_Dir.keys():
            MAE_LD_TOT.append(Linear_Dir[f'{g}']['KPI_TOT']['MAE_TOT'])
            MAE_LD_FL.append(Linear_Dir[f'{g}']['KPI_FL']['MAE_FL'])
            MAE_LD_PL.append(Linear_Dir[f'{g}']['KPI_PL']['MAE_PL'])
        for g in Linear_Ind.keys():
            MAE_LI_TOT.append(Linear_Ind[f'{g}']['KPI_TOT']['MAE_TOT'])
            MAE_LI_FL.append(Linear_Ind[f'{g}']['KPI_FL']['MAE_FL'])
            MAE_LI_PL.append(Linear_Ind[f'{g}']['KPI_PL']['MAE_PL'])
        for g in Exponential_Dir.keys():
            MAE_ED_TOT.append(Exponential_Dir[f'{g}']['KPI_TOT']['MAE_TOT'])
            MAE_ED_FL.append(Exponential_Dir[f'{g}']['KPI_FL']['MAE_FL'])
            MAE_ED_PL.append(Exponential_Dir[f'{g}']['KPI_PL']['MAE_PL'])
        for g in Exponential_Ind.keys():
            MAE_EI_TOT.append(Exponential_Ind[f'{g}']['KPI_TOT']['MAE_TOT']) 
            MAE_EI_FL.append(Exponential_Ind[f'{g}']['KPI_FL']['MAE_FL']) 
            MAE_EI_PL.append(Exponential_Ind[f'{g}']['KPI_PL']['MAE_PL']) 
        for g in Carnot.keys():
            MAE_C_TOT.append(Carnot[f'{g}']['KPI_TOT']['MAE_TOT'])
            MAE_C_FL.append(Carnot[f'{g}']['KPI_FL']['MAE_FL'])
            MAE_C_PL.append(Carnot[f'{g}']['KPI_PL']['MAE_PL'])  
        
        RMSE_LD_TOT = []
        RMSE_LI_TOT = []
        RMSE_ED_TOT = []
        RMSE_EI_TOT = []
        RMSE_C_TOT = []
        
        RMSE_LD_FL = []
        RMSE_LI_FL = []
        RMSE_ED_FL = []
        RMSE_EI_FL = []
        RMSE_C_FL = []
        
        RMSE_LD_PL = []
        RMSE_LI_PL = []
        RMSE_ED_PL = []
        RMSE_EI_PL = []
        RMSE_C_PL = []
        
        for g in Linear_Dir.keys():
            RMSE_LD_TOT.append(Linear_Dir[f'{g}']['KPI_TOT']['RMSE_TOT'])
            RMSE_LD_FL.append(Linear_Dir[f'{g}']['KPI_FL']['RMSE_FL'])
            RMSE_LD_PL.append(Linear_Dir[f'{g}']['KPI_PL']['RMSE_PL'])
        for g in Linear_Ind.keys():
            RMSE_LI_TOT.append(Linear_Ind[f'{g}']['KPI_TOT']['RMSE_TOT'])
            RMSE_LI_FL.append(Linear_Ind[f'{g}']['KPI_FL']['RMSE_FL'])
            RMSE_LI_PL.append(Linear_Ind[f'{g}']['KPI_PL']['RMSE_PL'])
        for g in Exponential_Dir.keys():
            RMSE_ED_TOT.append(Exponential_Dir[f'{g}']['KPI_TOT']['RMSE_TOT'])
            RMSE_ED_FL.append(Exponential_Dir[f'{g}']['KPI_FL']['RMSE_FL'])
            RMSE_ED_PL.append(Exponential_Dir[f'{g}']['KPI_PL']['RMSE_PL'])
        for g in Exponential_Ind.keys():
            RMSE_EI_TOT.append(Exponential_Ind[f'{g}']['KPI_TOT']['RMSE_TOT']) 
            RMSE_EI_FL.append(Exponential_Ind[f'{g}']['KPI_FL']['RMSE_FL']) 
            RMSE_EI_PL.append(Exponential_Ind[f'{g}']['KPI_PL']['RMSE_PL']) 
        for g in Carnot.keys():
            RMSE_C_TOT.append(Carnot[f'{g}']['KPI_TOT']['RMSE_TOT'])
            RMSE_C_FL.append(Carnot[f'{g}']['KPI_FL']['MAE_FL'])
            RMSE_C_PL.append(Carnot[f'{g}']['KPI_PL']['MAE_PL'])  
        
        "Plot TOT"
        figure1, axs1 = plt.subplots(3,figsize = (19,9.5))
        figure1.suptitle('$KPI_{TOT}$',fontsize = 15)
        
        axs1[0].boxplot([r2_LD_TOT, r2_LI_TOT, r2_ED_TOT, r2_EI_TOT, r2_C_TOT])
        axs1[0].set_xticks([1,2,3,4,5],["Linear Direct","Linear Indirect","Exponential Direct","Exponential Indirect","Carnot"])
        axs1[0].set_title('$R2_{TOT}$')   
        
        axs1[1].boxplot([MAE_LD_TOT, MAE_LI_TOT, MAE_ED_TOT, MAE_EI_TOT, MAE_C_TOT])
        axs1[1].set_xticks([1,2,3,4,5],["Linear Direct","Linear Indirect","Exponential Direct","Exponential Indirect","Carnot"])
        axs1[1].set_title('$MAE_{TOT}$')
        
        axs1[2].boxplot([RMSE_LD_TOT, RMSE_LI_TOT, RMSE_ED_TOT, RMSE_EI_TOT, RMSE_C_TOT])
        axs1[2].set_xticks([1,2,3,4,5],["Linear Direct","Linear Indirect","Exponential Direct","Exponential Indirect","Carnot"])
        axs1[2].set_title('$RMSE_{TOT}$')
        
        sns.set_theme(rc={'figure.figsize':(19,9.5)})
        plt.tight_layout()
        figure1.savefig(os.path.join('..',"Results",f"{Name}", f"{Name}_KPI_TOT.png")) #To modify to svg when defined
        plt.close()
        
        "Plot FL"
        figure2, axs2 = plt.subplots(3,figsize = (19,9.5))
        figure2.suptitle('$KPI_{FL}$',fontsize = 15)
        
        axs2[0].boxplot([r2_LD_FL, r2_LI_FL, r2_ED_FL, r2_EI_FL, r2_C_FL])
        axs2[0].set_xticks([1,2,3,4,5],["Linear Direct","Linear Indirect","Exponential Direct","Exponential Indirect","Carnot"])
        axs2[0].set_title('$R2_{FL}$')   
        
        axs2[1].boxplot([MAE_LD_FL, MAE_LI_FL, MAE_ED_FL, MAE_EI_FL, MAE_C_FL])
        axs2[1].set_xticks([1,2,3,4,5],["Linear Direct","Linear Indirect","Exponential Direct","Exponential Indirect","Carnot"])
        axs2[1].set_title('$MAE_{FL}$')
        
        axs2[2].boxplot([RMSE_LD_FL, RMSE_LI_FL, RMSE_ED_FL, RMSE_EI_FL, RMSE_C_FL])
        axs2[2].set_xticks([1,2,3,4,5],["Linear Direct","Linear Indirect","Exponential Direct","Exponential Indirect","Carnot"])
        axs2[2].set_title('$RMSE_{FL}$')
        
        sns.set_theme(rc={'figure.figsize':(19,9.5)})
        plt.tight_layout()
        figure2.savefig(os.path.join('..',"Results",f"{Name}", f"{Name}_KPI_FL.png")) #To modify to svg when whitched 
        plt.close()
        
        "Plot PL"
        figure3, axs3 = plt.subplots(3,figsize = (19,9.5))
        figure3.suptitle('$KPI_{PL}$',fontsize = 15)
        
        axs3[0].boxplot([r2_LD_PL, r2_LI_PL, r2_ED_PL, r2_EI_PL, r2_C_PL])
        axs3[0].set_xticks([1,2,3,4,5],["Linear Direct","Linear Indirect","Exponential Direct","Exponential Indirect","Carnot"])
        axs3[0].set_title('$R2_{PL}$')   
        
        axs3[1].boxplot([MAE_LD_PL, MAE_LI_PL, MAE_ED_PL, MAE_EI_PL, MAE_C_PL])
        axs3[1].set_xticks([1,2,3,4,5],["Linear Direct","Linear Indirect","Exponential Direct","Exponential Indirect","Carnot"])
        axs3[1].set_title('$MAE_{PL}$')
        
        axs3[2].boxplot([RMSE_LD_PL, RMSE_LI_PL, RMSE_ED_PL, RMSE_EI_PL, RMSE_C_PL])
        axs3[2].set_xticks([1,2,3,4,5],["Linear Direct","Linear Indirect","Exponential Direct","Exponential Indirect","Carnot"])
        axs3[2].set_title('$RMSE_{PL}$')
        
        
        sns.set_theme(rc={'figure.figsize':(19,9.5)})
        plt.tight_layout()
        figure3.savefig(os.path.join('..',"Results",f"{Name}", f"{Name}_KPI_PL.png")) #To modify to svg when defined 
        plt.close()
        

#%% Load Tests-----------------------------------------------------------------

def load_test2(Models, df, curve, Name):
    
    Test = {}
    import json
    
    "Create Folder"
    if not os.path.exists(os.path.join('..',"Results",f"{Name}")):
        os.mkdir(os.path.join('..',"Results",f"{Name}"))
    else:
        pass
    
#%% Test H01D01----------------------------------------------------------------
        
    #Test['H01D01'] = kpi_h01d01(Models, df, curve)
    
#%% Test H01D02----------------------------------------------------------------
        
    #Test['H01D02'] = kpi_h01d02(Models, df, curve)
    
#%% Test H01N------------------------------------------------------------------
        
    # Test['H01N - mod A'] = kpi_h01n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    # Test['H01N - mod B'] = kpi_h01n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    # Test['H01N - mod C'] = kpi_h01n(Models, df, curve, indirect_model = "C method")
    
#%% Test H02D01----------------------------------------------------------------
        
    # Test['H02D01'] = kpi_h02d01(Models, df, curve)
    
#%% Test H02D02----------------------------------------------------------------
        
    # Test['H02D02'] = kpi_h02d02(Models, df, curve)
    
#%% Test H02N------------------------------------------------------------------
        
    Test['H02N - mod A'] = kpi_h02n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    #Test['H02N - mod B'] = kpi_h02n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H02N - mod C'] = kpi_h02n(Models, df, curve, indirect_model = "C method")
    
#%% Test H03D01----------------------------------------------------------------
        
    # Test['H03D01'] = kpi_h03d01(Models, df, curve)
    
#%% Test H03D02----------------------------------------------------------------
        
    # Test['H03D02'] = kpi_h03d02(Models, df, curve)
    
#%% Test H03N------------------------------------------------------------------
        
    # Test['H03N - mod A'] = kpi_h03n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    # Test['H03N - mod B'] = kpi_h03n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    # Test['H03N - mod C'] = kpi_h03n(Models, df, curve, indirect_model = "C method")
    
#%% Test H04D01----------------------------------------------------------------
        
    # Test['H04D01'] = kpi_h04d01(Models, df, curve)
    
#%% Test H04D02----------------------------------------------------------------
        
    # Test['H04D02'] = kpi_h04d02(Models, df, curve)
    
#%% Test H04N------------------------------------------------------------------
        
    Test['H04N - mod A'] = kpi_h04n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    # Test['H04N - mod B'] = kpi_h04n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H04N - mod C'] = kpi_h04n(Models, df, curve, indirect_model = "C method")
    
#%% Test H05D01----------------------------------------------------------------
        
    # Test['H05D01'] = kpi_h05d01(Models, df, curve)
    
#%% Test H05D02----------------------------------------------------------------
        
    # Test['H05D02'] = kpi_h05d02(Models, df, curve)
    
#%% Test H05N------------------------------------------------------------------
        
    Test['H05N - mod A'] = kpi_h05n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    # Test['H05N - mod B'] = kpi_h05n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H05N - mod C'] = kpi_h05n(Models, df, curve, indirect_model = "C method")
    
#%% Test H06D01----------------------------------------------------------------
    
    # Test['H06D01'] = kpi_h06d01(Models, df, curve)
    
#%% Test H06D02----------------------------------------------------------------
        
    # Test['H06D02'] = kpi_h06d02(Models, df, curve)
    
#%% Test H06N------------------------------------------------------------------
        
    Test['H06N- mod A'] = kpi_h06n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    # Test['H06N- mod B'] = kpi_h06n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H06N- mod C'] = kpi_h06n(Models, df, curve, indirect_model = "C method")
    
#%% Test H07D01----------------------------------------------------------------
        
    # Test['H07D01'] = kpi_h07d01(Models, df, curve)
    
#%% Test H07D02----------------------------------------------------------------
        
    # Test['H07D02'] = kpi_h07d02(Models, df, curve)
    
#%% Test H07N------------------------------------------------------------------
        
    Test['H07N - mod A'] = kpi_h07n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    # Test['H07N - mod B'] = kpi_h07n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H07N - mod C'] = kpi_h07n(Models, df, curve, indirect_model = "C method")
    
#%% Test H08D01----------------------------------------------------------------
        
    # Test['H08D01'] = kpi_h08d01(Models, df, curve)
    
#%% Test H08D02----------------------------------------------------------------
        
    # Test['H08D02'] = kpi_h08d02(Models, df, curve)
    
#%% Test H08N------------------------------------------------------------------
        
    # Test['H08N - mod A'] = kpi_h08n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    # Test['H08N - mod B'] = kpi_h08n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    # Test['H08N - mod C'] = kpi_h08n(Models, df, curve, indirect_model = "C method")
    
#%% Test H09D01----------------------------------------------------------------
        
    # Test['H09D01'] = kpi_h09d01(Models, df, curve)
    
#%% Test H09D02----------------------------------------------------------------
        
    # Test['H09D02'] = kpi_h09d02(Models, df, curve)
    
#%% Test H09N------------------------------------------------------------------
        
    # Test['H09N - mod A'] = kpi_h09n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    # Test['H09N - mod B'] = kpi_h09n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    # Test['H09N - mod C'] = kpi_h09n(Models, df, curve, indirect_model = "C method")
        
#%% Test H10N------------------------------------------------------------------
        
    Test['H10N - mod A'] = kpi_h10n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    # Test['H10N - mod B'] = kpi_h10n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H10N - mod C'] = kpi_h10n(Models, df, curve, indirect_model = "C method")
    
#%% Test H11N------------------------------------------------------------------
        
    Test['H11N - mod A'] = kpi_h11n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    # Test['H11N - mod B'] = kpi_h11n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H11N - mod C'] = kpi_h11n(Models, df, curve, indirect_model = "C method")
    
#%% Test H12N------------------------------------------------------------------
        
    Test['H12N - mod A'] = kpi_h12n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
    # Test['H12N - mod B'] = kpi_h12n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
    Test['H12N - mod C'] = kpi_h12n(Models, df, curve, indirect_model = "C method")
    
#%% Save as Jason file --------------------------------------------------------
    
    with open(os.path.join('..',"Results",f"{Name}",f'{Name}_KPI.json'), 'w') as f:
     json.dump(Test, f)
    
    return Test
            
            
            
            
                    
                    
                
                
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            







