import pandas as pd
import os
from Code.models_classes import *
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#%% Definition of class for plots

class plot():
    
    def __init__(self, device, plot_data,res_real_data, df_real_data):
        
        self.device = device
        self.plot_data = plot_data
        self.res_real_data = res_real_data
        self.df_real_data = df_real_data
        
    def boxplot(self):
        
        #Create folder
        if not os.path.exists(os.path.join('..',"Results",self.device)):
            os.mkdir(os.path.join('..',"Results",self.device))
        else:
            pass
    
        #Set plot
        figure1, axs1 = plt.subplots(3,figsize = (19,9.5))
        figure1.suptitle('$KPI_{TOT}$',fontsize = 15)
        
        sns.set_theme(rc={'figure.figsize':(19,9.5)})
        plt.tight_layout()
        
        
        #Split the models among data available 
        self.ref_si_level = self. plot_data.reset_index(level=["model","plr_model","operation","kpi"])
        self.direct_linear = self.ref_si_level.loc[self.ref_si_level["plr_model"] == "direct_linear", ["model","plr_model","operation","kpi", self.device ]]
        self.direct_quadratic = self.ref_si_level.loc[self.ref_si_level["plr_model"] == "direct_quadratic", ["model","plr_model","operation","kpi", self.device ]]
        self.Mod_A = self.ref_si_level.loc[self.ref_si_level["plr_model"] == "ISO 13612-2 mod A", ["model","plr_model","operation","kpi", self.device ]]
        self.Mod_B = self.ref_si_level.loc[self.ref_si_level["plr_model"] == "ISO 13612-2 mod B", ["model","plr_model","operation","kpi",self.device ]]
        self.Mod_C = self.ref_si_level.loc[self.ref_si_level["plr_model"] == "method C", ["model","plr_model","operation","kpi",self.device ]]


        axs1[0].boxplot([self.direct_linear.loc[(self.direct_linear["kpi"] == "MAPE"), self.device],
             self.direct_quadratic.loc[(self.direct_quadratic["kpi"] == "MAPE" ) , self.device ],
             self.Mod_A.loc[(self.Mod_A["kpi"] == "MAPE"), self.device ], 
             self.Mod_B.loc[(self.Mod_B["kpi"] == "MAPE" ), self.device ], 
             self.Mod_C.loc[(self.Mod_C["kpi"] == "MAPE" ), self.device ]],showfliers = False)
        
        axs1[0].set_xticks([1,2,3,4,5],["Linear Direct","Linear Quadratic","ISO 13612-2 mod A","ISO 13612-2 mod B","method C" ])
        axs1[0].set_title('$MAE_{TOT}$')   
        
        axs1[1].boxplot([self.direct_linear.loc[(self.direct_linear["kpi"] == "RMSE" ), self.device ],
             self.direct_quadratic.loc[(self.direct_quadratic["kpi"] == "RMSE" ) , self.device ],
             self.Mod_A.loc[(self.Mod_A["kpi"] == "RMSE"), self.device ], 
             self.Mod_B.loc[(self.Mod_B["kpi"] == "RMSE" ), self.device ], 
             self.Mod_C.loc[(self.Mod_C["kpi"] == "RMSE" ), self.device ]],showfliers = False)
        
        axs1[1].set_xticks([1,2,3,4,5],["Linear Direct","Linear Quadratic","ISO 13612-2 mod A","ISO 13612-2 mod B","method C"])
        axs1[1].set_title('$RMSE_{TOT}$')   
        
        axs1[2].boxplot([self.direct_linear.loc[(self.direct_linear["kpi"] == "R2" ), self.device ],
             self.direct_quadratic.loc[(self.direct_quadratic["kpi"] == "R2" ) , self.device ],
             self.Mod_A.loc[(self.Mod_A["kpi"] == "R2"), self.device ], 
             self.Mod_B.loc[(self.Mod_B["kpi"] == "R2"), self.device ], 
             self.Mod_C.loc[(self.Mod_C["kpi"] == "R2" ), self.device ]],showfliers = False)
        
        axs1[2].set_xticks([1,2,3,4,5],["Linear Direct","Linear Quadratic","ISO 13612-2 mod A","ISO 13612-2 mod B","method C" ])
        axs1[2].set_title('$R2_{TOT}$')   
        
        figure1.savefig(os.path.join('..',"Results",self.device, f"{self.device}_KPI_TOT.png")) #To modify to svg when defined
        plt.close()
       
        
    def cop_pred_plot(self):
        
        if not os.path.exists(os.path.join('..',"Results",self.device)):
            os.mkdir(os.path.join('..',"Results",self.device))
        else:
            pass
    
        #Set plot
        figure1, axs1 = plt.subplots(1,figsize = (19,9.5))
        sns.set_theme(rc={'figure.figsize':(19,9.5)})
        plt.tight_layout()
        
        
        # self.ref_si_level = self. res_real_data.reset_index(level=["model","plr_model","operation","kpi"])
        
        for model_tag in ['01','02','03','04','05','06','07','08','09','10','11','12']:
            for plr_model in ["direct_linear","direct_quadratic","ISO 13612-2 mod A","ISO 13612-2 mod B","method C" ]:
                
                if model_tag in ["10","11","12"] and plr_model in ["direct_linear","direct_quadratic",]:
                    continue
                
                try:
                    self.COP_real = np.array(self.df_real_data["COP"])
                    self.COP_pred = np.array(self.res_real_data.loc[f"{model_tag}",f"{plr_model}", "TOT","COP"][self.device])
                    
                    try:
                        plt.plot(self.COP_real,self.COP_pred,"o", color = "orange", markeredgecolor = "black", label = "COP_pred")
                        plt.plot([0, 10], [0, 10], "k--", label = "Bisector")
                        plt.plot([0, 10], [0, 12], "k--", label = "Error +20%")
                    
                        plt.text( 6, 4.5, "-20%")
                        plt.plot([0, 10], [0, 8], "k--", label = "Error -20%")
                        plt.text( 6, 7.7, "+20%")
            
                        plt.xlabel("COP")
                        plt.xlim(0,10)
                        plt.ylim(0,10)
                        plt.ylabel('$COP_{pred}$')
                        plt.legend()
                    
                        plt.title(f"H {model_tag} {plr_model}")
                        plt.savefig(os.path.join('..',"Results",self.device, f"{self.device}_Plot_COP_{model_tag}_{plr_model}.png")) #To modify to svg when defined 
                        plt.close()
                        
                    except ValueError:
                            pass
                
                except ValueError and KeyError:
                    pass
    
    def Err_plr_plot(self):
        
        if not os.path.exists(os.path.join('..',"Results",self.device)):
            os.mkdir(os.path.join('..',"Results",self.device))
        else:
            pass
    
        #Set plot
        figure1, axs1 = plt.subplots(1,figsize = (19,9.5))
        sns.set_theme(rc={'figure.figsize':(19,9.5)})
        plt.tight_layout()
        
        for model_tag in ['01','02','03','04','05','06','07','08','09','10','11','12']:
            for plr_model in ["direct_linear","direct_quadratic","ISO 13612-2 mod A","ISO 13612-2 mod B","method C" ]:
                
                if model_tag in ["10","11","12"] and plr_model in ["direct_linear","direct_quadratic",]:
                    continue
                
                try:
                    self.COP_real = np.array(self.df_real_data["COP"])
                    self.COP_pred = np.array(self.res_real_data.loc[f"{model_tag}",f"{plr_model}", "TOT","COP"][self.device])
                    
                    self.Err =  self.COP_pred-self.COP_real
                    self.plr = self.df_real_data["PLR"]
                    

                    if not np.isnan(self.Err).all():    
                        plt.plot(self.plr,self.Err,"o", color = "blue", markeredgecolor = "black", label = "Error")
                        plt.xlabel("PLR")
                        plt.xlim(0.2,1.1)
                        # plt.ylim(-4,1)
                        plt.ylabel('$Err_{cop}$')
                        plt.legend()
                        plt.title(f"H {model_tag} {plr_model}")
                        plt.savefig(os.path.join('..',"Results",self.device, f"{self.device}_Plot_ERR_vs_PLR_{model_tag}_{plr_model}.png")) #To modify to svg when defined 
                        plt.close()
                    
                except ValueError and KeyError:
                    pass
                    
        
    def Err_SET_plot(self):
        
        if not os.path.exists(os.path.join('..',"Results",self.device)):
            os.mkdir(os.path.join('..',"Results",self.device))
        else:
            pass
    
        #Set plot
        figure1, axs1 = plt.subplots(1,figsize = (19,9.5))
        sns.set_theme(rc={'figure.figsize':(19,9.5)})
        plt.tight_layout()
        
        for model_tag in ['01','02','03','04','05','06','07','08','09','10','11','12']:
            for plr_model in ["direct_linear","direct_quadratic","ISO 13612-2 mod A","ISO 13612-2 mod B","method C" ]:
                
                if model_tag in ["10","11","12"] and plr_model in ["direct_linear","direct_quadratic",]:
                    continue
                
                try:
                    self.COP_real = np.array(self.df_real_data["COP"])
                    self.COP_pred = np.array(self.res_real_data.loc[f"{model_tag}",f"{plr_model}", "TOT","COP"][self.device])
                    
                    self.Err =  self.COP_pred-self.COP_real
                    self.SET= self.df_real_data["SET [°C]"]
                    
                    if not np.isnan(self.Err).all():   
                        plt.plot(self.SET,self.Err,"o", color = "green", markeredgecolor = "black", label = "Error")
                        # plt.ylim(-4,1)
                        plt.xlabel("SET")
                        plt.ylabel('$Err_{cop}$')
                        plt.legend()
                    
                        plt.title(f"H {model_tag} {plr_model}")
                        plt.savefig(os.path.join('..',"Results",self.device, f"{self.device}_Plot_ERR_vs_SET_{model_tag}_{plr_model}.png")) #To modify to svg when defined 
                        plt.close()
                    
                except ValueError and KeyError:
                    pass

    def COP_time_plot(self):
        
        if not os.path.exists(os.path.join('..',"Results",self.device)):
            os.mkdir(os.path.join('..',"Results",self.device))
        else:
            pass


        for model_tag in ['01','02','03','04','05','06','07','08','09','10','11','12']:
            for plr_model in ["direct_linear","direct_quadratic","ISO 13612-2 mod A","ISO 13612-2 mod B","method C" ]:
                
                if model_tag in ["10","11","12"] and plr_model in ["direct_linear","direct_quadratic",]:
                    continue
                
                try:
                    
                    COP_real = np.array(self.df_real_data["COP"])
                    COP_pred = np.array(self.res_real_data.loc[f"{model_tag}",f"{plr_model}", "TOT","COP"][self.device])
                    time = np.array(self.df_real_data["Time [min]"])
                    HC = np.array(self.df_real_data["Heat Cap COND [kW]"])
                    Pel_real = np.divide(COP_real, HC)
                    Pel_pred = np.divide(COP_pred, HC)
                    
                    
                    if not np.isnan(COP_pred).all(): 
                        
                        figure1, axs1 = plt.subplots(2,figsize = (19,9.5))
                        sns.set_theme(rc={'figure.figsize':(19,9.5)})
                        
                        axs1[0].set_title('COP vs Time')
                        axs1[0].plot(time, COP_real, label = "COP actual")
                        axs1[0].plot(time, COP_pred, label = "COP pred")
                        axs1[0].set_xlabel("Time [min]")
                        axs1[0].set_xlim(0,2500)
                        axs1[0].set_ylabel("COP actual")
                        axs1[0].legend()
                        
                        axs1[1].set_title('Power vs Time')
                        axs1[1].plot(time, HC, label = "Heat Capacity")
                        axs1[1].plot(time, Pel_real, label = "Power real [kW]")
                        axs1[1].plot(time, Pel_pred, label = "Power pred [kW]")
                        axs1[1].set_ylabel("Heat Capacity[kW] - Electrical power [kW]")
                        axs1[1].set_xlabel("Time [min]")
                        axs1[1].set_xlim(0,2500)
                        axs1[1].legend()
                        
                        figure1.savefig(os.path.join('..',"Results",self.device, f"{self.device}_Plot_COP_vs_Time_{model_tag}_{plr_model}.png")) #To modify to svg when defined 
                        plt.close(figure1)
                
                except ValueError:
                    pass
                    
                        
#%% Test models

devices = [
      # "Galletti MLI 18 kW",
      # "Galletti MLI 22 kW",
      # "Galletti MLI 26 kW",
      # "Galletti MLI 30 kW",
      # "WPL_A_HK 07 Premium",
      "Eneren NAW 006",
      # "Eneren NAW 006  All Raw Data",
      # "Eneren NAW 006  Filter on catalogue Data",     
     ]
 
models = ["0" + str(i) for i in range(1,10)] + ["10","11","12"]
plr_models = [
              "direct_linear",
              "direct_quadratic",
              "ISO 13612-2 mod A",
              "ISO 13612-2 mod B",
              "method C"
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
            #  ["06",model_h06],
            #  ["07",model_h07],
            # # ["08",model_h08],
            # # ["09",model_h09],
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
    dev.cop_pred_plot()
    dev.Err_plr_plot()
    dev.Err_SET_plot()
    dev.COP_time_plot()
        
# b = res.loc[:,:,"TOT","RMSE"]
# a = [[m,d["KPI_TOT"]["RMSE_TOT"]]for m,d in KPI.items()]





















 