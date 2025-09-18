import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

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
        figure1, axs1 = plt.subplots(2,figsize = (19,9.5))
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
        axs1[0].set_title('$MAPE_{TOT}$')   
        
        axs1[1].boxplot([self.direct_linear.loc[(self.direct_linear["kpi"] == "RMSE" ), self.device ],
             self.direct_quadratic.loc[(self.direct_quadratic["kpi"] == "RMSE" ) , self.device ],
             self.Mod_A.loc[(self.Mod_A["kpi"] == "RMSE"), self.device ], 
             self.Mod_B.loc[(self.Mod_B["kpi"] == "RMSE" ), self.device ], 
             self.Mod_C.loc[(self.Mod_C["kpi"] == "RMSE" ), self.device ]],showfliers = False)
        
        axs1[1].set_xticks([1,2,3,4,5],["Linear Direct","Linear Quadratic","ISO 13612-2 mod A","ISO 13612-2 mod B","method C"])
        axs1[1].set_title('$RMSE_{TOT}$')   
        
        figure1.savefig(os.path.join('..',"Results",self.device, f"{self.device}_KPI_TOT.png")) #To modify to svg when defined
        plt.close()
       
        
    def cop_pred_plot(self, var):
        
        if not os.path.exists(os.path.join('..',"Results",self.device)):
            os.mkdir(os.path.join('..',"Results",self.device))
        else:
            pass
    
        #Set plot
        figure1, axs1 = plt.subplots(1,figsize = (19,9.5))
        sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
        plt.tight_layout()
        
        
        # self.ref_si_level = self. res_real_data.reset_index(level=["model","plr_model","operation","kpi"])
        
        for model_tag in ['01','02','03','04','05','06','07','08','09','10','11','12']:
            for plr_model in ["direct_linear","direct_quadratic","ISO 13612-2 mod A","ISO 13612-2 mod B","method C" ]:
                
                if model_tag in ["10","11","12"] and plr_model in ["direct_linear","direct_quadratic",]:
                    continue
                
                try:
                    self.COP_real = np.array(self.df_real_data["COP"])
                    self.COP_pred = np.array(self.res_real_data.loc[f"{model_tag}",f"{plr_model}", "TOT","COP"][self.device])
                    self.var = np.array(self.df_real_data[f"{var}"])
                    
                    try:
                        plt.scatter(self.COP_real,self.COP_pred, c = self.var ,cmap='plasma', label = "COP_pred")
                        # plt.scatter(self.COP_real,self.COP_pred, c = self.var ,cmap='viridis', edgecolors = "black", label = "COP_pred")
                        plt.plot([0, 10], [0, 10], "k--", label = "Bisector")
                        plt.plot([0, 10], [0, 12], "k--", label = "Error +20%")                    
                        plt.text( 6, 4.5, "-20%")
                        plt.plot([0, 10], [0, 8], "k--", label = "Error -20%")
                        plt.text( 6, 7.7, "+20%")
                        cbar = plt.colorbar()
                        cbar.set_label(f"{var}")
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
        
        
    
    def Err_plr_plot(self,var):
        
        if not os.path.exists(os.path.join('..',"Results",self.device)):
            os.mkdir(os.path.join('..',"Results",self.device))
        else:
            pass
    
        #Set plot
        figure1, axs1 = plt.subplots(1,figsize = (19,9.5))
        sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
        plt.tight_layout()
        
        for model_tag in ['01','02','03','04','05','06','07','08','09','10','11','12']:
            for plr_model in ["direct_linear","direct_quadratic","ISO 13612-2 mod A","ISO 13612-2 mod B","method C" ]:
                
                if model_tag in ["10","11","12"] and plr_model in ["direct_linear","direct_quadratic",]:
                    continue
                
                try:
                    self.COP_real = np.array(self.df_real_data["COP"])
                    self.COP_pred = np.array(self.res_real_data.loc[f"{model_tag}",f"{plr_model}", "TOT","COP"][self.device])
                    
                    self.Err = (self.COP_pred-self.COP_real)/self.COP_real
                    self.plr = self.df_real_data["PLR"]
                    self.var = np.array(self.df_real_data[f"{var}"])

                    if not np.isnan(self.Err).all():    
                        plt.scatter(self.plr,self.Err,c = self.var ,cmap='plasma', edgecolors = "black", label = "Error")
                        plt.xlabel("PLR")
                        plt.xlim(0.2,1.1)
                        plt.ylim(-1,1)
                        cbar = plt.colorbar()
                        cbar.set_label(f"{var}")
                        plt.ylabel('$Err_{cop}$')
                        plt.legend()
                        plt.title(f"H {model_tag} {plr_model}")
                        plt.savefig(os.path.join('..',"Results",self.device, f"{self.device}_Plot_ERR_vs_PLR_{model_tag}_{plr_model}.png")) #To modify to svg when defined 
                        plt.close()
                       
                    
                except ValueError and KeyError:
                    pass
              
        
    def Err_SET_plot(self,var):
        
        if not os.path.exists(os.path.join('..',"Results",self.device)):
            os.mkdir(os.path.join('..',"Results",self.device))
        else:
            pass
    
        #Set plot
        figure1, axs1 = plt.subplots(1,figsize = (19,9.5))
        sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
        plt.tight_layout()
        
        for model_tag in ['01','02','03','04','05','06','07','08','09','10','11','12']:
            for plr_model in ["direct_linear","direct_quadratic","ISO 13612-2 mod A","ISO 13612-2 mod B","method C" ]:
                
                if model_tag in ["10","11","12"] and plr_model in ["direct_linear","direct_quadratic",]:
                    continue
                
                try:
                    self.COP_real = np.array(self.df_real_data["COP"])
                    self.COP_pred = np.array(self.res_real_data.loc[f"{model_tag}",f"{plr_model}", "TOT","COP"][self.device])
                    
                    self.Err = (self.COP_pred-self.COP_real)/self.COP_real
                    self.plr = self.df_real_data["PLR"]
                    self.SET= self.df_real_data["SET [°C]"]
                    self.var = np.array(self.df_real_data[f"{var}"])
                    
                    if not np.isnan(self.Err).all():   
                        plt.scatter(self.SET,self.Err,c = self.var ,cmap='cividis', edgecolors = "black", label = "Error")
                    
                        plt.xlabel("SET")
                        plt.ylabel('$Err_{cop}$')
                        plt.legend()
                        plt.ylim(-1,1)
                        cbar = plt.colorbar()
                        cbar.set_label(f"{var}")
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
                    Pel_real = np.array(self.df_real_data["Pow [kW]"])
                    time = np.array(self.df_real_data["Time [min]"])
                    HC_real = np.array(self.df_real_data["Heat Cap COND [kW]"])
                    HC_pred = np.multiply(COP_pred,Pel_real)
                    
                    # Pel_pred = np.divide(COP_pred, HC)
                    
                    
                    if not np.isnan(COP_pred).all(): 
                        
                        figure1, axs1 = plt.subplots(2,figsize = (19,9.5))
                        sns.set_theme(rc={'figure.figsize':(19,9.5)})
                        figure1.suptitle(f"{model_tag}_{plr_model}")
                        
                        axs1[0].set_title('COP vs Time')
                        axs1[0].plot(time, COP_real, label = "COP actual")
                        axs1[0].plot(time, COP_pred, label = "COP pred")
                        axs1[0].set_xlabel("Time [min]")
                        # axs1[0].set_xlim(150,1200)
                        axs1[0].set_ylabel("COP actual vs COP pred")
                        axs1[0].legend()
                        
                        axs1[1].set_title('Power vs Time')
                        # axs1[1].plot(time, Pel_real, label = "Pow [kW]")
                        axs1[1].plot(time, HC_real, label = "HC real [kW]", c = "blue")
                        axs1[1].plot(time, HC_pred, label = "HC pred [kW]", c ="green")
                        axs1[1].set_ylabel("Heat Capacity [kW]")
                        axs1[1].set_xlabel("Time [min]")
                        # axs1[1].set_xlim(150,1200)
                        axs1[1].legend()
                        
                        figure1.savefig(os.path.join('..',"Results",self.device, f"{self.device}_Plot_COP_and_Power_vs_Time_{model_tag}_{plr_model}.png")) #To modify to svg when defined 
                        plt.close(figure1)
                
                except ValueError:
                    pass
                
 
    def Err_GRAD_plot(self,var,grad):
        
        if not os.path.exists(os.path.join('..',"Results",self.device)):
            os.mkdir(os.path.join('..',"Results",self.device))
        else:
            pass
    
        #Set plot
        figure1, axs1 = plt.subplots(1,figsize = (19,9.5))
        sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
        plt.tight_layout()
        
        for model_tag in ['01','02','03','04','05','06','07','08','09','10','11','12']:
            for plr_model in ["direct_linear","direct_quadratic","ISO 13612-2 mod A","ISO 13612-2 mod B","method C" ]:
                
                if model_tag in ["10","11","12"] and plr_model in ["direct_linear","direct_quadratic",]:
                    continue
                
                try:
                    self.COP_real = np.array(self.df_real_data["COP"])
                    self.COP_pred = np.array(self.res_real_data.loc[f"{model_tag}",f"{plr_model}", "TOT","COP"][self.device])
                    self.Err = (self.COP_pred-self.COP_real)/self.COP_real
                    if grad == "EL":
                        self.Grad = self.df_real_data["Gradient EL"]
                    elif grad == "HC":
                        self.Grad = self.df_real_data["Gradient HC"]
                    self.var = np.array(self.df_real_data[f"{var}"])

                    if not np.isnan(self.Err).all():    
                        plt.scatter(self.Grad,self.Err,c = self.var ,cmap='plasma', label = "Error")
                        plt.xlabel("Gradient")
                        plt.xlim(-6,6)
                        plt.ylim(-2,2)
                        cbar = plt.colorbar()
                        cbar.set_label(f"{var}")
                        plt.ylabel('$Err_{cop}$')
                        plt.legend()
                        plt.title(f"H {model_tag} {plr_model}")
                        plt.savefig(os.path.join('..',"Results",self.device, f"{self.device}_Plot_ERR_vs_GRAD_{model_tag}_{plr_model}.png")) #To modify to svg when defined 
                        plt.close()
                       
                    
                except ValueError and KeyError:
                    pass
    
        
                    
                        





