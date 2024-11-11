import pandas as pd
import os
from models import *

"Import Data" 
import numpy as np
from sklearn import linear_model

df = pd.read_excel(os.path.join('..', '1--data', 'Galletti MLI 18 kW.xlsx'), sheet_name="SetData")
curve=pd.read_excel(os.path.join('..', '1--data', 'Galletti MLI 18 kW.xlsx'), sheet_name="curve")
Model={}

# "Divide between part load and full load operative points"
# df_FL = df[df['PLF']==1]
# df_PL= df[df['PLF']!=1]

# "Import data as Arrays - Full Load"
# SET_FL = np.array(df_FL["SET [°C]"])
# SExT_FL = np.array(df_FL["SExT [°C]"])
# Sfr_FL = np.array(df_FL["SFR [l/s]"])
# LET_FL = np.array(df_FL["LET [°C]"])
# LExT_FL = np.array(df_FL["LExT [°C]"])
# LFR_FL = np.array(df_FL["LFR [kg/s]"])
# HC_FL = np.array(df_FL["Heat Abs EVA [kW[]"])
# PLF_FL = np.array(df_FL["PLF"])
# COP_FL = np.array(df_FL["COP"])

# "Create matrix and full load calculations"
# LExT_SET_FL = LExT_FL-SET_FL
# LExT_SET_2_FL = (LExT_FL-SET_FL)**2
# cost = np.ones(len(HC_FL))
# X_FL = np.column_stack([cost,SET_FL,Sfr_FL,LExT_SET_FL,LExT_SET_2_FL])
# Y_FL = COP_FL

# model_reg_FL = linear_model.LinearRegression().fit(X_FL, Y_FL)


# "Import data as Arrays - Part Load"
# SET_PL = np.array(df_PL["SET [°C]"])
# SExT_PL = np.array(df_PL["SExT [°C]"])
# Sfr_PL = np.array(df_PL["SFR [l/s]"])
# LET_PL = np.array(df_PL["LET [°C]"])
# LExT_PL = np.array(df_PL["LExT [°C]"])
# LFR_FL = np.array(df_PL["LFR [kg/s]"])
# HC_PL = np.array(df_PL["Heat Abs EVA [kW[]"])
# PLF_PL = np.array(df_PL["PLF"])
# COP_PL = np.array(df_PL["COP"])

# "Create matrix and part load calculations"
# LExT_SET_PL = LExT_PL-SET_PL
# LExT_SET_2_PL = (LExT_PL-SET_PL)**2
# cost = np.ones(len(HC_PL))
# X_PL = np.column_stack([cost,SET_PL,Sfr_PL,LExT_SET_PL,LExT_SET_2_PL])

# COP_FL_pred = model_reg_FL.predict(X_PL)

# "Method 1: f_cop by linear regression"
# f_COP_1 = COP_PL/COP_FL_pred
# PLF_1=np.ones(len(PLF_PL))

# for i in range(len(PLF_PL)):
#     if PLF_PL [i] >= 0.25:
#         PLF_1[i]=1;
#     else:
#         PLF_1[i]=PLF_PL[i]/(0.9*4*PLF_PL+0.1)

# COP_1PL = PLF_1*COP_FL_pred
        
# "Method 2: f_cop derived by curves"
# PLF_curve = np.array(curve["X"])
# f_COP_curve = np.array(curve["f_cop"])
# f_COP_2 = np.interp(PLF_PL, PLF_curve, f_COP_curve)

# "Method 3: f_cop calculated"
# a=1/PLF_PL-1
# b=PLF_PL-1
# c=1/f_COP_1-1
# X3=np.column_stack([a,b])

# model_reg_3 = linear_model.LinearRegression().fit(X3,c)
# coeff_3 = model_reg_3.coef_
# intercept_3 = model_reg_3.intercept_
# f_COP_3 = np.ones(len(PLF_PL))

# for m in range(len(PLF_PL)):
#     f_COP_3[m] = PLF_PL[m]/(intercept_3+coeff_3[0]*PLF_PL[m]+coeff_3[1]*PLF_PL[m]**2)



#%% H01D01---------------------------------------------------------------------

H01D01 = model_h01d01(df)
Model['H01D01'] = H01D01
 
#%% H01D02---------------------------------------------------------------------

H01D02 = model_h01d02(df)
Model['H01D02'] = H01D02
 
#%% H01N  ---------------------------------------------------------------------

H01N_A, H01N_f1, H01 = model_h01d02(df)
Model['H01D02'] = H01D02
 
# fig, axs1 = plt.subplots(1,1, figsize = (19,9.5))
# axs1.scatter(Y, Y_pred, edgecolor = 'k', label='COP')
# axs1.set_xlabel('to mare')
# axs1.axline((0, 0), slope=1, color="black", linestyle=(0, (5, 5)))
# axs1.axline((0, 0), slope=0.7, color="black", linestyle=(0, (5, 5)), label = 'CI 30%')
# axs1.axline((0, 0), slope=1.3, color="black", linestyle=(0, (5, 5)), )
# axs1.set_xlim([0, 6.5])
# axs1.set_ylim([0, 6.5])
# axs1.set_title('sono ebete')
# axs1.legend()
# fig.savefig('model_2.png', dpi = 600)


