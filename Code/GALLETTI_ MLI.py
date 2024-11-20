import pandas as pd
import os
from models import *
from kpi import *
import numpy as np
# import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

#%%----------------------------------------------------------------------------

"Import Data" 
df = pd.read_excel(os.path.join('..', 'Data', 'Galletti MLI 18 kW.xlsx'), sheet_name="SetData")
curve=pd.read_excel(os.path.join('..', 'Data', 'Galletti MLI 18 kW.xlsx'), sheet_name="curve")
 
Models = load_models(df, curve)
KPI = load_test(df, curve)



# fig1, axs1 = plt.subplots(3, figsize = (19,9.5))
# fig1.suptitle("Models Performance")


# sns.set_theme(rc={'figure.figsize':(19,9.5)})
# fig1.tight_layout()



# #R2_ranges = ('[0;0.6[', '[0.6;0.7[', '[0.7;0.8[', '[0.8;0.9[', '[0.9;0.92[', '[0.92;0.94[', '[0.94;0.96[', '[0.96;0.98[', '[0.98;0.1]')
# R2_ranges = [0, 0.6, 0.7, 0.8, 0.9, 0.92, 0.94, 0.96, 0.98, 1]
# R2=[]
# MAE = []
# RMSE =  []
# for i in KPI:
#     R2.append(KPI[i]['r2'])
#     MAE.append(KPI[i]['MAE'])
#     RMSE.append(KPI[i]['RMSE'])
    
# axs1[0].hist(R2, bins= R2_ranges)
# axs1[1].hist(MAE)
# axs1[2].hist(RMSE)    

# # Add some text for labels, title and custom x-axis tick labels, etc.
# # axs1[0].set_xlabel('Intervallo di errore relativo')
# # axs1[0].set_ylabel('% edifici')
# # axs1[0].set_xticks(x + width, error_ranges)
# # axs1[0].set_ylim([0, 30])
# # axs1[0].legend()



# import seaborn as sns
# z=KPI["H01D01"]["COP_pred"]-COP



# # plot
# fig, ax = plt.subplots()
# ax.hexbin(x=df["SET [°C]"],y=df["LET [°C]"],C=z,cmap="copper")

# plt.show()



















 