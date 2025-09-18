import pandas as pd
import os
from Code.models_classes import *
# from Code.models_classes_modified import *
from Code.plot_classes import *
from sklearn import linear_model
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


def correlation(res):
    
    df = {"COP": np.array(res["COP"]),
          "SET": np.array(res["SET [°C]"]),
          "Delta":  np.array(res["Delta"]),
          "Delta2": np.array(res["Delta2"]),
          "PLR": np.array(res["PLR"])}
    
    df = pd.DataFrame(df)
    corrMatrix = df.corr()
    return corrMatrix

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
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID9 35-45°C LExT - 5 min - 3D int",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID9 35-45°C LExT - 5 min - Stationary",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID9 35-45°C LExT - 5 min - Start",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID9 35-45°C LExT - 5 min -Stop",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID24 35-45°C LExT",
      # "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - ID24 35-45°C LExT - Filter on catalogue",
      # "Valliant A+ 5kW  ID5 01-11-2022_28-02-2023",
      "Valliant A+ 5kW  ID9 01-11-2022_28-02-2023",
      # "Valliant A+ 5kW  ID24 01-11-2022_28-02-2023"
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
    curve=pd.read_excel(os.path.join('..', 'Data', dev + '.xlsx'), sheet_name="curve")
    
    for model_tag, model in [
            # ["01",model_h01],
             ["02",model_h02],
            # ["03",model_h03],
             # ["04",model_h04],
            #  ["05",model_h05],
             # ["06",model_h06],
            #  ["07",model_h07],
            # # # ["08",model_h08],
            # # #  ["09",model_h09],
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

performance = res_real_data.drop("COP", level = 3)
performance.to_excel(os.path.join('..','Result Analysis',"Performance" + ".xlsx"))

#%%Post processing
for dev in devices:
    plot_data = res_real_data.drop("COP", level = "kpi")
    plot_data = plot_data.astype(float)
    plot_data.dropna(inplace = True)
    dev = plot(dev, plot_data, res_real_data, df_real_data) 
    # dev.boxplot()
    # dev.cop_pred_plot("SET [°C]")
    # dev.cop_pred_plot("Delta")
    # dev.cop_pred_plot("Delta2")
    dev.cop_pred_plot("PLR")
    # dev.cop_pred_plot("Index")
    # dev.cop_pred_plot("LExT [°C]")
    # dev.cop_pred_plot("LET [°C]")
    # dev.cop_pred_plot("START and STOP")
    # dev.cop_pred_plot("Gradient HC")
    # dev.cop_pred_plot("Defrost")
    # dev.cop_pred_plot("PLR")
    # dev.cop_pred_plot("Pow [kW]") 
    # dev.cop_pred_plot("Heat Cap COND [kW]")
    # dev.cop_pred_plot("DeltaTW")
    dev.Err_plr_plot("SET [°C]")
    # dev.Err_GRAD_plot("PLR","HC")
    # dev.Err_SET_plot("COP")
    # dev.COP_time_plot()


#%% Correction factor for transitory calculation

# for dev in devices:
#     for plr_model in plr_models:
            
#             #Method 1: linear regression on gradients
#             COP_real = np.array(df_real_data["COP"])
#             COP_pred = np.array(res_real_data.loc[f"{model_tag}",f"{plr_model}", "TOT","COP"][dev])
#             # Err =  (COP_pred - COP_real) / COP_real
#             Err =  COP_real / COP_pred
#             # Err =  COP_real - COP_pred
#             Grad_SET =  np.gradient(np.array(df_real_data["SET [°C]"]))
#             Grad_Delta1 =  np.gradient(np.array(df_real_data["Delta"]))
#             Grad_Delta2 =  np.gradient(np.array(df_real_data["Delta2"]))
#             Grad_PLR =  np.gradient(np.array(df_real_data["PLR"]))
#             # Grad_EL =  df_real_data["Gradient EL"]
#             # SET =  df_real_data["SET [°C]"]
            
#             CR = df_real_data
#             CR = CR.drop(['Status'], axis = 1)
#             # CR = CR
#             # {"Err": Err, 
#             #       "Gradient EL": Grad_EL, 
#             #       "Gradient HC": Grad_HC,
#             #       "SET": SET, "COP_pred": COP_pred,
#             #       "COP_real" : COP_real,
#             #       "Gradient HC2": Grad_HC**2, 
#             #       "Gradient EL2": Grad_EL**2,
#             #       "HC": df_real_data["Heat Cap COND [kW]"],
#             #       "Pow": df_real_data["Pow [kW]"],
#             #       "SET": df_real_data["Heat Cap COND [kW]"}
            
#             CR = pd.DataFrame(CR)
#             CR["Err"] = Err
#             CR['COP_pred'] = COP_pred
#             CR["Grad SET"] = Grad_SET
#             CR["Grad Delta1"] = Grad_Delta1
#             CR["Grad Delta2"] = Grad_Delta2
#             CR["Grad PLR"] = Grad_PLR
#             CR = CR.loc[:, ~CR.columns.str.contains('^Unnamed')] 
#             CR = CR.dropna()
#             test_pearson = CR.corr(method = 'pearson')
#             test_spearman = CR.corr(method = 'spearman')
            
            
            
#             # df_real_data.to_excel(os.path.join('..','Result Analysis',"err gradient" + ".xlsx"))
#             # z = np.polyfit(Grad_EL,Err, 1)
#             # p = np.poly1d(z)
            
#             # cr = p(Grad_EL)
     
#             X = np.column_stack([np.ones(len(CR["Gradient EL"])), 
#                                  # CR["Gradient EL"],
#                                  # CR["Gradient HC"],
#                                  # CR["SET [°C]"],
#                                  # CR["LExT [°C]"],
#                                  # CR["Heat Cap COND [kW]"],
#                                  # CR["Pow [kW]"],
#                                  # CR["HC"],
#                                  CR["Grad SET"],
#                                  CR["Grad Delta1"],
#                                  CR["Grad Delta2"],
#                                  CR["Grad PLR"]
#                                  # CR["Gradient EL"]*CR["COP_pred"],
#                                  # CR["Gradient EL"]/ CR["Pow [kW]"]*CR["COP_pred"],
#                                  # CR["Gradient HC"]/CR["Gradient EL"]
#                                  # # CR["Pow"]
#                                  ])
            
#             model_reg_CR = linear_model.LinearRegression().fit(X, np.array(CR["Err"]))
#             CR_pred = model_reg_CR.predict(X)
#             # CR_pred =  matrix_CR["Gradient HC"]/matrix_CR["Gradient EL"]
            
          
            
#             figure1, axs = plt.subplots(1,2,figsize = (19,9.5))
#             sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
#             plt.tight_layout()
            
#             axs[0].scatter(CR["Pow [kW]"],CR["Err"], c = 'red', label = "Error")
#             axs[1].scatter(CR["Heat Cap COND [kW]"],CR["Err"], c = 'blue', label = "Error")
#             axs[0].scatter(CR["Pow [kW]"],CR_pred, label = "polinomial fit", c = "green")
#             axs[1].scatter(CR["Heat Cap COND [kW]"],CR_pred, c = 'green', label = "Error")
#             axs[0].set_xlabel("power")
#             axs[1].set_xlabel("HC")
#             # # plt.xlim(-6,6)
#             axs[0].set_ylim(0,2)
#             axs[1].set_ylim(0,2)
#             axs[0].set_xlabel("Power EL")
#             axs[1].set_xlabel("HC")
#             # # cbar = plt.colorbar()
#             # # cbar.set_label(f"{var}")
#             # plt.ylabel('$Err_{cop}$')
#             # plt.legend()
#             # plt.title(f"H {model_tag} {plr_model}")
            
#             #Method 2: linear interpolation on Catalogue COPS
            
            
            
            
                
#             figure2, axs1 = plt.subplots(1,figsize = (19,9.5))
#             sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
#             plt.tight_layout()
#             # COP_correct = matrix_CR["COP_pred"]/(1 + CR_pred)
#             # COP_correct = CR["COP_pred"] + CR_pred
#             COP_correct = CR["COP_pred"] * CR_pred
#             plt.scatter(CR["Err"], CR_pred, c = CR["Gradient HC"],cmap='plasma',label = "Correction")
#             plt.xlabel("err")
#             plt.ylabel("err_pred")
#             # plt.plot([0, 10], [0, 10], "k--", label = "Bisector")
#             # plt.plot([0, 10], [0, 12], "k--", label = "Error +20%")
#             # plt.plot([0, 10], [0, 8], "k--", label = "Error -20%")
#             cbar = plt.colorbar()
#             # plt.xlim(0,2)
#             # plt.ylim(0,2)
            
#             figure3, axs1 = plt.subplots(1,figsize = (19,9.5))
#             sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
#             plt.tight_layout()
#             # COP_correct = CR["COP_pred"] + CR_pred
#             plt.scatter(CR["COP"], COP_correct, c = CR["Gradient HC"],cmap='plasma',label = "Correction")
#             plt.plot([0, 10], [0, 10], "k--", label = "Bisector")
#             plt.plot([0, 10], [0, 12], "k--", label = "Error +20%")
#             plt.plot([0, 10], [0, 8], "k--", label = "Error -20%")
#             plt.xlim(0,10)
#             plt.ylim(0,10)
            

#%% #Error analysis
for dev in devices:
    
    if not os.path.exists(os.path.join('..',"Correlation Analyisis",dev)):
        os.mkdir(os.path.join('..',"Correlation Analyisis",dev))
    else:
        pass
    df_real_data = pd.read_excel(os.path.join('..', 'Data', dev + '.xlsx'), sheet_name="Test")
    Err = (COP -  df_real_data["COP"])/df_real_data["COP"]
    ErrTest = {"Time" : df_real_data["Time"],
                "COP real": df_real_data["COP"],
               "COP pred": COP,
               "Err_COP": Err,
               "SET": np.array(df_real_data["SET [°C]"]),
               "Delta":  np.array(df_real_data["Delta"]),
               "Delta2": np.array(df_real_data["Delta2"]),
               "PLR": np.array(df_real_data["PLR"]),
               "Power": np.array(df_real_data["Pow [kW]"]),
                "HC": np.array(df_real_data["Heat Cap COND [kW]"]),
                # "Original Index": np.array(df_real_data["Original Index"]),
                # "Gradient_EL": np.array(df_real_data["Gradient_EL"])
                }
                             
    ErrTest = pd.DataFrame(ErrTest)
    # ErrTest.set_index("Original Index", inplace= True)
    ErrTest1 = ErrTest[ErrTest["Err_COP"] > 0.25]
    ErrTest2 = ErrTest[ErrTest["Err_COP"] <= 0.25]
    ErrTest1.to_csv(os.path.join('..', 'Correlation Analyisis',f'{dev}',f"{dev}"+" "+"ErrTest1.csv"), index=False)
    ErrTest2 .to_csv(os.path.join('..', 'Correlation Analyisis',f'{dev}',f"{dev}"+" "+"ErrTest2.csv"), index=False)

#%% Plot Bar

# print(os.path.isfile(os.path.join('..','Result Analysis', "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW","Filtered data analysis-paper UIT vs 1.01" + '.xlsx')))
# kpi = pd.read_excel(os.path.join('..', 'Result Analysis',  "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW", "Filtered data analysis-paper UIT vs 1.01" + '.xlsx'))
# # kpi = pd.read_excel(os.path.join('..', 'Result Analysis',  "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW", "All data analysis-paper UIT" + '.xlsx'))

# figure1, axs1 = plt.subplots(2,2,figsize = (19,9.5))
# sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
# plt.tight_layout
# font = 20
     
# model = ["H02D01","H02D02","H02NA","H02NB","H02NC"]
# kpis = ["RMSE","MAPE","R2","Err_SCOP"]

# RMSE = kpi.loc[kpi['kpi'] == "RMSE"]
# MAPE = kpi.loc[kpi['kpi'] == "MAPE"]
# R2 = kpi.loc[kpi['kpi'] == "R2"]
# Err_SCOP = kpi.loc[kpi['kpi'] == "Err SCOP"]

# barWidth = 0.2
# br1 = np.arange(len(RMSE["ID5"])) 
# br2 = [x + barWidth for x in br1] 
# br3 = [x + barWidth for x in br2] 


# axs1[0,0].bar(br1, np.array(RMSE["ID5"]), width = barWidth, label = 'ID5')
# axs1[0,0].bar(br2, np.array(RMSE["ID9"]), width = barWidth, label = 'ID9')
# axs1[0,0].bar(br3, np.array(RMSE["ID24"]), width = barWidth, label = 'ID24')
# axs1[0,0].set_xticks(br2, model, fontsize = font)
# axs1[0,0].tick_params(axis='y', labelsize= font)
# axs1[0,0].set_ylabel("RMSE", fontsize = font)
# # axs1[0,0].legend(fontsize = font)

# axs1[0,1].bar(br1, np.array(MAPE["ID5"]), width = barWidth, label = 'ID5')
# axs1[0,1].bar(br2, np.array(MAPE["ID9"]), width = barWidth, label = 'ID9')
# axs1[0,1].bar(br3, np.array(MAPE["ID24"]), width = barWidth, label = 'ID24')
# axs1[0,1].set_xticks(br2, model, fontsize = font)
# axs1[0,1].tick_params(axis='y', labelsize= font)
# axs1[0,1].set_ylabel("MAPE", fontsize = font)
# # axs1[0,1].legend(fontsize = font)

# axs1[1,0].bar(br1, np.array(R2["ID5"]), width = barWidth, label = 'ID5')
# axs1[1,0].bar(br2, np.array(R2["ID9"]), width = barWidth, label = 'ID9')
# axs1[1,0].bar(br3, np.array(R2["ID24"]), width = barWidth, label = 'ID24')
# axs1[1,0].set_xticks(br2, model, fontsize = font)
# axs1[1,0].tick_params(axis='y', labelsize= font)
# axs1[1,0].set_ylabel("R2", fontsize = font)
# # axs1[1,0].legend(fontsize = font)

# axs1[1,1].bar(br1, np.array(Err_SCOP["ID5"]), width = barWidth, label = 'ID5')
# axs1[1,1].bar(br2, np.array(Err_SCOP["ID9"]), width = barWidth, label = 'ID9')
# axs1[1,1].bar(br3, np.array(Err_SCOP["ID24"]), width = barWidth, label = 'ID24')
# axs1[1,1].set_xticks(br2, model, fontsize = font)
# axs1[1,1].tick_params(axis='y', labelsize= font)
# axs1[1,1].set_ylabel("Err SCOP", fontsize = font)
# axs1[1,1].legend(fontsize = font)


# figure1.savefig(os.path.join('..','Result Analysis', "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW","Filtered data anlysis.svg"))
# figure1.savefig(os.path.join('..','Result Analysis', "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW","All data analysis.svg"))
# plt.close()

# # %% Plot Standard

# figure1, axs1 = plt.subplots(figsize = (19,9.5))
# sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')

# font = 25

# #Create plot
# xs = np.array(curve["X"])
# ys = np.array(curve["f_cop"])
# name = ['A','B','C','D']
# f_cop_a =np.array([1,1,1,1,0])


# axs1.plot(xs,f_cop_a,color ="green", label =" Method 1", linewidth = 2)
# axs1.plot(xs,ys,color ="blue", label =" Method 2", linewidth = 2, marker = "o")

# # Add Labels to the points
# i = 0
# for x,y in zip(xs,ys):
#     label = name [i]
#     plt.annotate(label, # this is the text
#                  (x,y), # these are the coordinates to position the label
#                  textcoords="offset points", # how to position the text
#                  xytext=(0,10), # distance from text to points (x,y)
#                  ha='center',
#                  fontsize = font) # horizontal alignment can be left, right or center

#     i += 1
#     if i == 4:
#         break



# # Customize plot
# axs1.set_xlabel("PLR", fontsize = font)
# axs1.set_xlim(0,1.1)
# axs1.tick_params(axis='x', labelsize= font)
# axs1.set_ylabel("$f_{cop}$", fontsize = font)
# axs1.set_ylim(0)
# axs1.tick_params(axis='y', labelsize= font)
# axs1.legend(fontsize = font)
# axs1.set_title("Standard ISO 13612-2 curves", fontsize = font)
# figure1.savefig(os.path.join('..','Result Analysis', "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW","Standard plot.svg"))
# plt.tight_layout
# plt.close()

# #%% Plot Bar vs 2

# print(os.path.isfile(os.path.join('..','Result Analysis', "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW","Filtered data analysis-paper UIT vs 1.01" + '.xlsx')))
# kpi1 = pd.read_excel(os.path.join('..', 'Result Analysis',  "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW", "All data analysis-paper UIT vs 1.01" + '.xlsx'))
# kpi2 = pd.read_excel(os.path.join('..', 'Result Analysis',  "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW", "Filtered data analysis-paper UIT vs 1.01" + '.xlsx'))


# figure1, axs1 = plt.subplots(4,2,figsize = (19,9.5))
# sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')

# font = 20
     
# model = ["Dir-L","Dir-Q","Ind-B","Ind-C"]
# kpis = ["RMSE","MAPE","R2","Err_SCOP"]

# RMSE_all = kpi1.loc[kpi1['kpi'] == "RMSE"]
# RMSE_all = RMSE_all.loc[RMSE_all["Model"] != "H02N-A"]
# MAPE_all = kpi1.loc[kpi1['kpi'] == "MAPE"]
# MAPE_all = MAPE_all.loc[MAPE_all["Model"] != "H02N-A"]
# R2_all = kpi1.loc[kpi1['kpi'] == "R2"]
# R2_all = R2_all.loc[R2_all["Model"] != "H02N-A"]
# Err_SCOP_all = kpi1.loc[kpi1['kpi'] == "Err SCOP"]
# Err_SCOP_all = Err_SCOP_all.loc[Err_SCOP_all["Model"] != "H02N-A"]

# RMSE_fil = kpi2.loc[kpi2['kpi'] == "RMSE"]
# RMSE_fil = RMSE_fil.loc[RMSE_fil["Model"] != "H02N-A"]
# MAPE_fil = kpi2.loc[kpi2['kpi'] == "MAPE"]
# MAPE_fil = MAPE_fil.loc[MAPE_fil["Model"] != "H02N-A"]
# R2_fil = kpi2.loc[kpi2['kpi'] == "R2"]
# R2_fil = R2_fil.loc[R2_fil['Model'] != "H02N-A"]
# Err_SCOP_fil = kpi1.loc[kpi2['kpi'] == "Err SCOP"]
# Err_SCOP_fil = Err_SCOP_fil.loc[Err_SCOP_fil['Model'] != "H02N-A"]

# barWidth = 0.2
# br1 = np.arange(len(RMSE_all["ID5"])) 
# br2 = [x + barWidth for x in br1] 
# br3 = [x + barWidth for x in br2] 


# axs1[0,0].bar(br1, np.array(RMSE_all["ID5"]), width = barWidth, label = 'ID5')
# axs1[0,0].bar(br2, np.array(RMSE_all["ID9"]), width = barWidth, label = 'ID9')
# axs1[0,0].bar(br3, np.array(RMSE_all["ID24"]), width = barWidth, label = 'ID24')
# axs1[0,0].set_xticks(br2, model, fontsize = font)
# axs1[0,0].tick_params(axis='y', labelsize= font)
# axs1[0,0].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
# axs1[0,0].set_ylabel("RMSE [-]", fontsize = font)
# axs1[0,0].set_title("KPIs All Conditions",fontsize = font )
# axs1[0,0].set_ylim(0,1.5)
# # axs1[0,0].legend(fontsize = font)

# axs1[1,0].bar(br1, np.array(MAPE_all["ID5"]), width = barWidth, label = 'ID5')
# axs1[1,0].bar(br2, np.array(MAPE_all["ID9"]), width = barWidth, label = 'ID9')
# axs1[1,0].bar(br3, np.array(MAPE_all["ID24"]), width = barWidth, label = 'ID24')
# axs1[1,0].set_xticks(br2, model, fontsize = font)
# axs1[1,0].tick_params(axis='y', labelsize= font)
# axs1[1,0].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
# axs1[1,0].set_ylabel("MAPE [-]", fontsize = font)
# axs1[1,0].set_ylim(0,0.15)
# # axs1[0,1].legend(fontsize = font)

# #deleate 0 
# R2_correct_ID9_all = []
# R2_correct_ID24_all = []

# for i in np.array(R2_all["ID9"]):
#     if i <= 0:
#         R2_correct_ID9_all.append(0)
#     else:
#         R2_correct_ID9_all.append(i)

# for i in np.array(R2_all["ID24"]):
#     if i <= 0:
#         R2_correct_ID24_all.append(0)
#     else:
#         R2_correct_ID24_all.append(i)

        
# axs1[2,0].bar(br1, np.array(R2_all["ID5"]), width = barWidth, label = 'ID5')
# axs1[2,0].bar(br2, R2_correct_ID9_all, width = barWidth, label = 'ID9')
# axs1[2,0].bar(br3, R2_correct_ID24_all, width = barWidth, label = 'ID24')
# axs1[2,0].set_xticks(br2, model, fontsize = font)
# axs1[2,0].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
# axs1[2,0].tick_params(axis='y', labelsize= font)
# axs1[2,0].set_ylabel("R2 [-]", fontsize = font)
# axs1[2,0].set_ylim(0,0.8)
# # axs1[1,0].legend(fontsize = font)

# axs1[3,0].bar(br1, np.array(Err_SCOP_all["ID5"]), width = barWidth, label = 'ID5')
# axs1[3,0].bar(br2, np.array(Err_SCOP_all["ID9"]), width = barWidth, label = 'ID9')
# axs1[3,0].bar(br3, np.array(Err_SCOP_all["ID24"]), width = barWidth, label = 'ID24')
# axs1[3,0].set_xticks(br2, model, fontsize = font)
# axs1[3,0].tick_params(axis='y', labelsize= font)
# axs1[3,0].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
# axs1[3,0].set_ylabel("Err SCOP [-]", fontsize = font)
# axs1[3,0].set_ylim(-0.05,0.1)
# # axs1[3,0].legend(fontsize = font)


# #Filter graphs
# axs1[0,1].bar(br1, np.array(RMSE_fil["ID5"]), width = barWidth, label = 'ID5')
# axs1[0,1].bar(br2, np.array(RMSE_fil["ID9"]), width = barWidth, label = 'ID9')
# axs1[0,1].bar(br3, np.array(RMSE_fil["ID24"]), width = barWidth, label = 'ID24')
# axs1[0,1].set_xticks(br2, model, fontsize = font)
# axs1[0,1].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
# axs1[0,1].tick_params(axis='y', labelsize= font)
# axs1[0,1].set_title("KPIs Steady-state Conditions",fontsize = font)
# axs1[0,1].legend(bbox_to_anchor=(1.05, 1),
#                          loc='upper left', borderaxespad=0.,fontsize = font)
# axs1[0,1].set_ylim(0,1.5)
# # axs1[0,1].set_ylabel("RMSE [-]", fontsize = font)

# axs1[1,1].bar(br1, np.array(MAPE_fil["ID5"]), width = barWidth, label = 'ID5')
# axs1[1,1].bar(br2, np.array(MAPE_fil["ID9"]), width = barWidth, label = 'ID9')
# axs1[1,1].bar(br3, np.array(MAPE_fil["ID24"]), width = barWidth, label = 'ID24')
# axs1[1,1].set_xticks(br2, model, fontsize = font)
# axs1[1,1].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
# axs1[1,1].tick_params(axis='y', labelsize= font)
# axs1[1,1].set_ylim(0,0.15)
# # axs1[1,1].set_ylabel("MAPE [-]", fontsize = font)

# #deleate 0 
# R2_correct_ID9_fil = []
# R2_correct_ID24_fil = []

# for i in np.array(R2_fil["ID9"]):
#     if i <= 0:
#         R2_correct_ID9_fil.append(0)
#     else:
#         R2_correct_ID9_fil.append(i)

# for i in np.array(R2_fil["ID24"]):
#     if i <= 0:
#         R2_correct_ID24_fil.append(0)
#     else:
#         R2_correct_ID24_fil.append(i)
        
# axs1[2,1].bar(br1, np.array(R2_fil["ID5"]), width = barWidth, label = 'ID5')
# axs1[2,1].bar(br2, R2_correct_ID9_fil, width = barWidth, label = 'ID9')
# axs1[2,1].bar(br3, R2_correct_ID24_fil, width = barWidth, label = 'ID24')
# axs1[2,1].set_xticks(br2, model, fontsize = font)
# axs1[2,1].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
# axs1[2,1].tick_params(axis='y', labelsize= font)
# axs1[2,1].set_ylim(0,0.8)
# # axs1[2,1].set_ylabel("R2 [-]", fontsize = font)

# axs1[3,1].bar(br1, np.array(Err_SCOP_fil["ID5"]), width = barWidth, label = 'ID5')
# axs1[3,1].bar(br2, np.array(Err_SCOP_fil["ID9"]), width = barWidth, label = 'ID9')
# axs1[3,1].bar(br3, np.array(Err_SCOP_fil["ID24"]), width = barWidth, label = 'ID24')
# axs1[3,1].set_xticks(br2, model, fontsize = font)
# axs1[3,1].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
# axs1[3,1].tick_params(axis='y', labelsize= font)
# axs1[3,1].set_ylim(-0.05,0.1)

# # axs1[3,1].set_ylabel("Err SCOP [-]", fontsize = font)
# # axs1[3,1].legend(fontsize = font)

# plt.tight_layout()
# figure1.tight_layout()

# figure1.savefig(os.path.join('..','Result Analysis', "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW","New data anlysis.svg"))
# plt.close()














 