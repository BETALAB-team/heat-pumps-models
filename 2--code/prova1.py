import pandas as pd
import os
import numpy as np
from sklearn import linear_model

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

X=np.column_stack([cost,SET,Sfr,LExT_SET,LExT_SET_sq,PLF])
# Xt=np.transpose(X)
Y=COP
#%%
model = linear_model.LinearRegression()
model_reg = model.fit(X, Y)

coefficienti_1 = model_reg.coef_
intercetta_1 = model_reg.intercept_

R2_1 = model_reg.score(X, Y)









