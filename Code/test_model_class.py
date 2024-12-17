import pandas as pd
import os
from Code.models_classes import *
import numpy as np
# import seaborn as sns
#import matplotlib.pyplot as plt

#%%----------------------------------------------------------------------------

devices = [
    "Galletti MLI 18 kW",
    # "Galletti MLI 22 kW",
    # "Galletti MLI 26 kW",
    # "Galletti MLI 30 kW",
    ]

models = ["0" + str(i) for i in range(1,10)] + ["10","11","12"]
plr_models = ["direct_linear",
              "direct_quadratic",
              "ISO 13612-2 mod A",
              "ISO 13612-2 mod B",
              "C method"
              ]
dfs_levels = ["TOT","PL","FL"]
kpis = ["RMSE","MAE","R2"]

res = pd.DataFrame(index=pd.MultiIndex.from_product([
    models,plr_models,dfs_levels,kpis
    ],names=("model","plf_model","operation","kpi")), columns = devices)

res_real_data = pd.DataFrame(index=pd.MultiIndex.from_product([
    models,plr_models,["TOT"],kpis
    ],names=("model","plf_model","operation","kpi")), columns = devices)


for dev in devices:
    "Import Data" 
    df = pd.read_excel(os.path.join('..', 'Data', dev + '.xlsx'), sheet_name="SetData")
    df_dati_reali = pd.read_excel(os.path.join('..', 'Data', dev + '.xlsx'), sheet_name="TestData")
    curve=pd.read_excel(os.path.join('..', 'Data', dev + '.xlsx'), sheet_name="curve")
    
    for model_tag, model in [
            ["01",model_h01],
            ["02",model_h02],
            ["03",model_h03],
            ["04",model_h04],
            ["05",model_h05],
            ["06",model_h06],
            ["07",model_h07],
            ["08",model_h08],
            ["09",model_h09],
            ["10",model_h10],
            ["11",model_h11],
            ["12",model_h12],
            ]:
        for m in plr_models:
            
            if model_tag in ["10","11","12"] and m in ["direct_linear","direct_quadratic",]:
                continue
            
            mod = model(plr_method=m)
            mod.set_curve_df(curve)
            mod.train_model(df)
                        
            results = mod.test_with_catalogue()
            for op in dfs_levels:
                res.loc[model_tag,m,op,"MAE"][dev] = results[op]["MAE_"+op]
                res.loc[model_tag,m,op,"RMSE"][dev] = results[op]["RMSE_"+op]
                res.loc[model_tag,m,op,"R2"][dev] = results[op]["r2_"+op]
                
            results_real_data = mod.test_with_data(df_dati_reali)
            for op in ["TOT"]:
                res_real_data.loc[model_tag,m,op,"MAE"][dev] = results_real_data[op]["MAE_"+op]
                res_real_data.loc[model_tag,m,op,"RMSE"][dev] = results_real_data[op]["RMSE_"+op]
                res_real_data.loc[model_tag,m,op,"R2"][dev] = results_real_data[op]["r2_"+op]
            

b = res.loc[:,:,"TOT","RMSE"]
a = [[m,d["KPI_TOT"]["RMSE_TOT"]]for m,d in KPI.items()]


#%%


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



















 