import pandas as pd
import os
import matplotlib.pyplot as plt

from code.models import model_h01d01, model_h01d02

df=pd.read_excel(os.path.join('1--Data','Galletti MLI 18 kW.xlsx'), sheet_name="SetData")

Y_predict, Y, MSE, RMSE = model_h01d01(df)

"Plot"
fig,[ax1,ax2]=plt.subplots(nrows=1,ncols=2)
ax1.plot(Y_predict,Y)

