# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 10:33:32 2024

@author: benafra10167
"""
import numpy as np
import pandas as pd
import os
from scipy.optimize import fmin_bfgs
import matplotlib.pyplot as plt

df = pd.read_excel(os.path.join('..', '1--data', 'Galletti MLI 18 kW.xlsx'), sheet_name="SetData")

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
#A0 =[31.8154644222407, 0.00107507522941172, -0.00225321950989943, 1.14471337349467, -0.723569969853511, -25.4177693645696]
A0=np.ones(6)*1.5


def fun(x0, xdata, ydata):
      
    Y_pred =  x0[0]*np.exp(x0[1]*xdata[:,0] + x0[2]*xdata[:,1]) + x0[3]*xdata[:,0]/xdata[:,1] + x0[4] *xdata[:,2] +x0[5]
    res = sum((ydata-Y_pred)**2)   
    return res


#A, cov = curve_fit(fun, X, Y, p0 = np.ones(6))
A = fmin_bfgs(fun, A0, args = (X, Y), full_output= 1)

#Y_pred = fun(X,A[0],A[1], A[2], A[3], A[4], A[5])
# res = sum((Y-Y_pred)**2)

# fig, ax = plt.subplots()
# ax.scatter(Y, Y_pred, edgecolor = 'k', label='COP')
# #ax.plot(X[:,0],Y_pred)

# M=X[0,:]
# M= np.reshape(M, (1,3))
# prova=fun(M, 31.8154644222407, 0.00107507522941172, -0.00225321950989943, 1.14471337349467, -0.723569969853511, -25.4177693645696 )