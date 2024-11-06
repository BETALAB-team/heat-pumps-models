import pandas as pd
import os
import matplotlib.pyplot as plt

from models import model_h01d01, model_h01d02

df=pd.read_excel(os.path.join(r'1--data','Galletti MLI 18 kW.xlsx'), sheet_name="SetData")

Y_predict, Y, MSE, RMSE = model_h01d01(df)


"Plot"
fig,ax=plt.subplots(nrows=1,ncols=1)
fig.scatter()
ax.plot(Y_predict,Y)

