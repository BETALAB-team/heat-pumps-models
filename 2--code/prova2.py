import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
import seaborn as sns

# df = pd.read_excel(os.path.join('..', '1--data', 'Galletti MLI 18 kW.xlsx'), sheet_name="SetData")
df = pd.read_excel(r'C:/Users/benafra10167/OneDrive - Università degli Studi di Padova/PHD/2--Calculations/1--Processing HP CMP 2024/1--NewData/heat-pumps-models/1--data/Galletti MLI 18 kW.xlsx', sheet_name="SetData")
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
PLF_sq=PLF**2

X=np.column_stack([cost,SET,Sfr,LExT_SET,LExT_SET_sq,PLF,PLF_sq])
# Xt=np.transpose(X)
Y=COP
#%%
model = linear_model.LinearRegression()
model_reg = model.fit(X, Y)

coefficienti = model_reg.coef_
intercetta = model_reg.intercept_

R2 = model_reg.score(X, Y)

#%%
Y_pred = model_reg.predict(X)
MAE = mean_absolute_error(Y, Y_pred)
RMSE = root_mean_squared_error(Y, Y_pred)

#%%
# Apply default theme:
sns.set_theme(rc={'figure.figsize':(38.5,21)}, font_scale=2)

"Plot"
fig,ax=plt.subplots(nrows=1,ncols=1)
plt.title('COP real vs COP predicted')
plt.xlabel('COP real [/]')
plt.ylabel('COP predicted [/]')
ax.scatter(Y,Y_pred,c='r',edgecolor='k',label='COP')
ax.plot([0,5,7],[0,5,7],'k--',label='Bisector')
ax.plot([0,5,7],[0,3.5,4.9],'k-.',label='-30%')
ax.plot([0,5,7],[0,6.5,9.1],'k-.',label='+30%')
plt.xlim(1,6.5)
plt.ylim(1,6.5)
ax.legend()
ax.grid(True)


#%%
fig, axs1 = plt.subplots(1,1, figsize = (19,9.5))

axs1.scatter(Y, Y_pred, edgecolor = 'k', label='COP')
axs1.set_xlabel('to mare')
axs1.axline((0, 0), slope=1, color="black", linestyle=(0, (5, 5)))
axs1.axline((0, 0), slope=0.7, color="black", linestyle=(0, (5, 5)), label = 'CI 30%')
axs1.axline((0, 0), slope=1.3, color="black", linestyle=(0, (5, 5)), )
axs1.set_xlim([0, 6.5])
axs1.set_ylim([0, 6.5])
axs1.set_title('sono ebete')
axs1.legend()
fig.savefig('model_2.png', dpi = 600)




# axs4[0,0].bar(avg_damage_level_bulbasaur.keys(), avg_damage_level_bulbasaur.values())
# axs4[0,0].set_xlabel('Pokemon level')
# axs4[0,0].set_ylabel('Avg damage')
# axs4[0,0].set_ylim([0, 16])
# axs4[0,0].set_title('Bulbasaur')