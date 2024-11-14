import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error, root_mean_squared_error,r2_score

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
    COP_pred = Models['H01D01']['scikit model'].predict(np.column_stack([cost,SET,Sfr,LExT_SET,LExT_SET_2,PLF]))
    
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
