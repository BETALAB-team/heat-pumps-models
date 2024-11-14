import pandas as pd
import os
from models import *


df = pd.read_excel(os.path.join('..', '1--data', 'Galletti MLI 18 kW.xlsx'), sheet_name="SetData")
curve=pd.read_excel(os.path.join('..', '1--data', 'Galletti MLI 18 kW.xlsx'), sheet_name="curve")

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

"Carnot efficency full load calculations"
    
SET_data = 7 #[°C]
LExT_data = 35 #[°C]
curve = curve.set_index(curve['SET'])
COP_data = curve.loc[SET_data, 'COP_fl']
COP_carnot = (LExT_data + 273.15 )/ (LExT_data - SET_data)
eta_FL = COP_data / COP_carnot # second principle efficency for full load data point
   
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
  
"Create function to calculate COP_FL_pred" 

X=np.column_stack([SET_PL, LExT_PL, COP_PL])

def f_COP_fun_Carnot(X,eta_FL):
    
    SET_PL = X[:, 0]
    LExT_PL = X[:, 1]
    COP_PL = X[:, 2]
    COP_carnot_PL=np.ones(len(SET_PL))
    COP_FL_pred=np.ones(len(SET_PL))
    
    for i in range(len(LExT_PL)):
    
        if LExT_PL[i] <= SET_PL[i]:
            COP_carnot_PL[i]=50;
        else:
            COP_carnot_PL[i] = (273+ LExT_PL[i])/(LExT_PL[i] - SET_PL[i])
    
        COP_FL_pred[i] = COP_carnot_PL[i] * eta_FL
        
    f_COP_model_FL = COP_PL/ COP_FL_pred
    
    return f_COP_model_FL    

f_COP_model_FL =  f_COP_fun_Carnot(X,eta_FL)
f_COP_model_FL = lambda X, eta_FL:  f_COP_fun_Carnot(X, eta_FL)   

   