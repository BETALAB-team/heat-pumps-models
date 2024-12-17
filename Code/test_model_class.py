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
    # "WPL_A_HK 07 Premium",
     # "Eneren NAW 006"
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
    ],names=("model","plr_model","operation","kpi")), columns = devices)


for dev in devices:
    "Import Data" 
    df = pd.read_excel(os.path.join('..', 'Data', dev + '.xlsx'), sheet_name="SetData")
    curve=pd.read_excel(os.path.join('..', 'Data', dev + '.xlsx'), sheet_name="curve")
    
    for model_tag, model in [
            # ["01",model_h01],
            ["02",model_h02],
            # ["03",model_h03],
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

# b = res.loc[:,:,"TOT","RMSE"]
# a = [[m,d["KPI_TOT"]["RMSE_TOT"]]for m,d in KPI.items()]


#%%
# import matplotlib.pyplot as plt
# def boxplot(devices):
    
#     for dev
    
# #Split the models among data available 
# ref_si_level = res.reset_index(level=["model","plr_model","operation","kpi"])
# direct_linear = ref_si_level.loc[ref_si_level["plr_model"] == "direct_linear", ["model","plr_model","operation","kpi","Galletti MLI 18 kW" ]]
# direct_quadratic = ref_si_level.loc[ref_si_level["plr_model"] == "direct_quadratic", ["model","plr_model","operation","kpi","Galletti MLI 18 kW" ]]
# Mod_A = ref_si_level.loc[ref_si_level["plr_model"] == "ISO 13612-2 mod A", ["model","plr_model","operation","kpi","Galletti MLI 18 kW" ]]
# Mod_B = ref_si_level.loc[ref_si_level["plr_model"] == "ISO 13612-2 mod B", ["model","plr_model","operation","kpi","Galletti MLI 18 kW" ]]
# Mod_C = ref_si_level.loc[ref_si_level["plr_model"] == "C method", ["model","plr_model","operation","kpi","Galletti MLI 18 kW" ]]

# figure1, axs1 = plt.subplots(3,figsize = (19,9.5))
# figure1.suptitle('$KPI_{TOT}$',fontsize = 15)

# axs1[0].boxplot([direct_linear[(direct_linear["kpi"] == "R2" ) & (direct_linear["operation"] == "TOT"), ["Galletti MLI 18 kW"]],
#                 direct_quadrqatic[(direct_quadratic["kpi"] == "R2" ) & (direct_quadratic["operation"] == "TOT"), ["Galletti MLI 18 kW"]],
#                 Mod_A[(Mod_A["kpi"] == "R2" ) & (Mod_A["operation"] == "TOT"), ["Galletti MLI 18 kW"]], 
#                 Mod_B[(Mod_A["kpi"] == "R2" ) & (Mod_B["operation"] == "TOT"), ["Galletti MLI 18 kW"]],
#                 Mod_C[(Mod_A["kpi"] == "R2" ) & (Mod_C["operation"] == "TOT"), ["Galletti MLI 18 kW"]]],showfliers = False)
# axs1[0].set_xticks([1,2,3,4,5],["Linear Direct","Linear Quadratic","ISO 13612-2 mod A","ISO 13612-2 mod B", ])
# axs1[0].set_title('$R2_{TOT}$')   
# #axs1[0].set_ylim(0.5,1) 

# axs1[1].boxplot([MAE_LD_TOT, MAE_LI_TOT, MAE_ED_TOT, MAE_EI_TOT],showfliers = False)
# axs1[1].set_xticks([1,2,3,4],["Linear Direct","Linear Indirect","Exponential Direct","Exponential Indirect"])
# axs1[1].set_title('$MAE_{TOT}$')
# #axs1[1].set_ylim(0,0.5)

# axs1[2].boxplot([RMSE_LD_TOT, RMSE_LI_TOT, RMSE_ED_TOT, RMSE_EI_TOT], showfliers = False)
# axs1[2].set_xticks([1,2,3,4],["Linear Direct","Linear Indirect","Exponential Direct","Exponential Indirect"])
# axs1[2].set_title('$RMSE_{TOT}$')
# #axs1[2].set_ylim(0.2,0.8) 

# sns.set_theme(rc={'figure.figsize':(19,9.5)})
# plt.tight_layout()
# figure1.savefig(os.path.join('..',"Results",f"{Name}", f"{Name}_KPI_TOT.png")) #To modify to svg when defined
# plt.close()




















 