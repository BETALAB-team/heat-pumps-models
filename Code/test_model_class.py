import pandas as pd
import os
from Code.models_classes import *
from Code.plot_classes import *
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


#%% Test models

devices = [
      # "Galletti MLI 18 kW",
      # "Galletti MLI 22 kW",
      # "Galletti MLI 26 kW",
      # "Galletti MLI 30 kW",
      # "WPL_A_HK 07 Premium",
      # "Eneren NAW 006 Old catalogue 1",
      # "Eneren NAW 006 Old catalogue 1 - Reversed",
      # "Eneren NAW 006 Old catalogue 2",
      # "Eneren NAW 006 Old catalogue 2 - Reversed",
      # "Eneren NAW 006  New catalogue",
      # "Eneren NAW 006  New catalogue - Reversed",
      # "Eneren NAW 006  New catalogue - PLR calculation",
      # "Eneren NAW 006  All Raw Data",
      # "Eneren NAW 006  Old - Filter on catalogue Data",
      # "Eneren NAW 006  New -  Filter on catalogue Data",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID5 Exp Points",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID5 35-45°C LExT",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID5 35-45°C LExT - Reversed",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID5 Catalogue"
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID5 35-45°C LExT - 5 min",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID53",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID9 35-45°C LExT",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID9  35°C LExT",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID9   All data",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID9 35-45°C LExT - 5 min",
      "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID9 35-45°C LExT - 5 min - new power",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID9 35-45°C LExT - 5 min - 3D int",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID9 35-45°C LExT - 5 min - Stationary",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID9 35-45°C LExT - 5 min - Start",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID9 35-45°C LExT - 5 min -Stop",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID24 35-45°C LExT",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID24 35-45°C LExT - Filter on catalogue",
      ]
 
models = ["0" + str(i) for i in range(1,10)] + ["10","11","12"]
plr_models = [
              "direct_linear",
              # "direct_quadratic",
              # "ISO 13612-2 mod A",
              # "ISO 13612-2 mod B",
              # "method C"
              ]

dfs_levels = ["TOT","PL","FL"]
kpis = ["RMSE","MAPE","R2"]

res = pd.DataFrame(index=pd.MultiIndex.from_product([
    models,plr_models,dfs_levels,kpis
    ],names=("model","plr_model","operation","kpi")), columns = devices, dtype = float)

res_real_data = pd.DataFrame(index=pd.MultiIndex.from_product([
    models,plr_models,["TOT"],kpis + ["COP"] + ["SCOP"]
    ],names=("model","plr_model","operation","kpi")), columns = devices)


for dev in devices:
    
    "Import Data" 
    df = pd.read_excel(os.path.join('..', 'Data', dev + '.xlsx'), sheet_name="SetData")
    df_real_data = pd.read_excel(os.path.join('..', 'Data', dev + '.xlsx'), sheet_name="Test")
    df_real_data = df_real_data[df_real_data["PLR"] <= 1]
    # df_real_data = df_real_data[df_real_data["Index"] == 1]
    curve=pd.read_excel(os.path.join('..', 'Data', dev + '.xlsx'), sheet_name="curve")
    
    for model_tag, model in [
            # ["01",model_h01],
             ["02",model_h02],
            # ["03",model_h03],
            #  ["04",model_h04],
            #  ["05",model_h05],
            #  ["06",model_h06],
            #  ["07",model_h07],
            # # ["08",model_h08],
            # #  ["09",model_h09],
            #  ["10",model_h10],
            #  ["11",model_h11],
            #  ["12",model_h12],
             ]:
        for m in plr_models:
            
            if model_tag in ["10","11","12"] and m in ["direct_linear","direct_quadratic",]:
                continue
            
            mod = model(plr_method=m)
            mod.set_curve_df(curve)
            mod.train_model(df)
                        
            results = mod.test_with_catalogue()
            results_real_data = mod.test_with_data(df_real_data)
            COP = mod.calc_with_data(df_real_data)
            SCOP = mod.calc_SCOP(df_real_data)
            
            for op in dfs_levels:
                res.loc[model_tag,m,op,"MAPE"][dev] = results[op]["MAPE_"+op]
                res.loc[model_tag,m,op,"RMSE"][dev] = results[op]["RMSE_"+op]
                res.loc[model_tag,m,op,"R2"][dev] = results[op]["r2_"+op]
                
            
            for op in ["TOT"]:
                res_real_data.loc[model_tag,m,op,"MAPE"][dev] = results_real_data[op]["MAPE_"+op]
                res_real_data.loc[model_tag,m,op,"RMSE"][dev] = results_real_data[op]["RMSE_"+op]
                res_real_data.loc[model_tag,m,op,"R2"][dev] = results_real_data[op]["r2_"+op]
                res_real_data.loc[model_tag,m,op,"COP"][dev] = COP
                res_real_data.loc[model_tag,m,op,"SCOP"][dev] = SCOP
        

for dev in devices:
    plot_data = res_real_data.drop("COP", level = "kpi")
    plot_data = plot_data.astype(float)
    plot_data.dropna(inplace = True)
    dev = plot(dev, plot_data, res_real_data, df_real_data) 
    # dev.boxplot()
    # dev.cop_pred_plot("SET [°C]")
    # dev.cop_pred_plot("Index")
    # dev.cop_pred_plot("LExT [°C]")
    # dev.cop_pred_plot("LET [°C]")
    dev.cop_pred_plot("Index")
    # dev.cop_pred_plot("PLR")
    # dev.cop_pred_plot("Pow [kW]")
    # dev.cop_pred_plot("Heat Cap COND [kW]")
    # dev.cop_pred_plot("DeltaTW")
    # dev.Err_plr_plot("SET [°C]")
    # dev.Err_SET_plot("PLR")
    # dev.COP_time_plot()
        






















 