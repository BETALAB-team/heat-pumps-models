import pandas as pd
import sklearn as sk
import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

from models import model_h01d01,model_h01d02

df=pd.read_excel('Galletti MLI 18 kW.xlsx', sheet_name="SetData")

Y_predict, Y, MSE, RMSE = model_h01d01(df)

for macchina in lista_macchine:
    for mod in [model_h01d01,model_h01d02]:
        res = mod(df)

"Plot"
fig,[ax1,ax2]=plt.subplots(nrows=1,ncols=2)
ax1.plot(Y_predict,Y)

