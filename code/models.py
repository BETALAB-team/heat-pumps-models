import pandas as pd
import sklearn as sk
import numpy as np
import math
import matplotlib_inline as plt
from sklearn.metrics import mean_squared_error

def model_h01d01(df):
    # Model H01D01
    "Import data as Arrays"

    SET=np.array(df["SET [°C]"])
    SExT=np.array(df["SExT [°C]"])
    Sfr=np.array(df["SFR [l/s]"])
    LET=np.array(df["LET [°C]"])
    LExT=np.array(df["LExT [°C]"])
    LFR=np.array(df["LFR [kg/s]"])
    HC=np.array(df["Heat Abs EVA [kW[]"])
    PLF=np.array(df["PLF"])
    COP=np.array(df["COP"])

    "Create matrix and calculations"
    LExT_SET=LExT-SET
    LExT_SET_sq=(LExT-SET)**2
    cost=np.ones(len(HC))

    X=np.column_stack([cost,SET,Sfr,LExT_SET,LExT_SET_sq,PLF])
    Xt=np.transpose(X)
    Y=COP

    A=np.matmul(np.linalg.inv(np.matmul(Xt,X)),np.matmul(Xt,Y))

    "Test and error calculation"
    Y_predict=np.matmul(X,A)
    MSE=mean_squared_error(Y, Y_predict)
    #MSE = np.square(np.subtract(Y,Y_predict)).mean() 
    RMSE = np.sqrt(MSE)
    
    return Y_predict, Y, MSE, RMSE

def model_h01d02(df):
    # Model H01D01
    "Import data as Arrays"

    SET=np.array(df["SET [°C]"])
    SExT=np.array(df["SExT [°C]"])
    Sfr=np.array(df["SFR [l/s]"])
    LET=np.array(df["LET [°C]"])
    LExT=np.array(df["LExT [°C]"])
    LFR=np.array(df["LFR [kg/s]"])
    HC=np.array(df["Heat Abs EVA [kW[]"])
    PLF=np.array(df["PLF"])
    COP=np.array(df["COP"])

    "Create matrix and calculations"
    LExT_SET=LExT-SET
    LExT_SET_sq=(LExT-SET)**2
    cost=np.ones(len(HC))

    X=np.column_stack([cost,SET,Sfr,LExT_SET,LExT_SET_sq,PLF])
    Xt=np.transpose(X)
    Y=COP

    A=np.matmul(np.linalg.inv(np.matmul(Xt,X)),np.matmul(Xt,Y))

    "Test and error calculation"
    Y_predict=np.matmul(X,A)
    MSE=mean_squared_error(Y, Y_predict)
    #MSE = np.square(np.subtract(Y,Y_predict)).mean() 
    RMSE = np.sqrt(MSE)
    
    return MSE, RMSE
    
    

    