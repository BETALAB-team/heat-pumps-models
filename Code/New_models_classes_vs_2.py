import os 
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error,r2_score,mean_absolute_percentage_error
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import linear_model
from scipy.signal import savgol_filter
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

#%% Model vs 2.0 class structure

class Heat_Pumps():
    
    def __init__(self,device):
        
        self.name, self.catalogue_data, self.source = device

        self.test = pd.read_excel(os.path.join('..','ExpData',f"{self.name}.xlsx"), sheet_name = "Sheet1")
        self.test = self.test.loc[:, ~self.test.columns.str.contains('^Unnamed')] 
        
        self.train_fl = pd.read_excel(os.path.join('..','Data',f"{self.catalogue_data}.xlsx"), sheet_name = "Full Load").astype(float)
        self.train = pd.read_excel(os.path.join('..','Data', f"{self.catalogue_data}.xlsx"), sheet_name = "SetData")
     
#%%#Plot method
    def plot_power_model(self,Pow_pred, status):
        
        #Create folder
        if not os.path.exists(os.path.join('..',"Results",self.name)):
            os.mkdir(os.path.join('..',"Results",self.name))
        else:
            pass
        
        if not os.path.exists(os.path.join('..',"Results",f"{self.name}","New_models")):
            os.mkdir(os.path.join('..',"Results",self.name,"New_models"))
        else:
            pass
    
    
        #Plot Power_pred vs Power_real 
        figure3, axs3 = plt.subplots(1, figsize = (19,9.5))
        sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
    
        plt.scatter(np.array(self.test_fil["Pow [kW]"]),Pow_pred, c = self.test_fil["PLR"], cmap='jet', label = "Power_model")
        plt.plot([0, 10], [0, 10], "k--", label = "Bisector")
        plt.plot([0, 10], [0, 12], "k--", label = "Error +20%")                    
        plt.text( 6, 4.5, "-20%")
        plt.plot([0, 10], [0, 8], "k--", label = "Error -20%")
        plt.text( 6, 7.7, "+20%")
        cbar = plt.colorbar()
        cbar.set_label("PLR")
        plt.xlabel("Power_exp [kW]")
        # plt.xlim(0,6)
        # plt.ylim(0,6)
        plt.ylabel('Power_model[kW]')
        plt.legend()
        plt.show()
        
        # plt.tight_layout()
        plt.savefig(os.path.join('..',"Results",f"{self.name}","New_models",f"NEW_MODEL_{status}.png"))
        plt.close()
            
#%% Plot method
    def plot_COP_model(self,COP_pred, status):
        
        #Create folder
        if not os.path.exists(os.path.join('..',"Results",self.name)):
            os.mkdir(os.path.join('..',"Results",self.name))
        else:
            pass
        
        if not os.path.exists(os.path.join('..',"Results",f"{self.name}","New_models")):
            os.mkdir(os.path.join('..',"Results",self.namedev,"New_models"))
        else:
            pass


        #Plot Power_pred vs Power_real 
        figure3, axs3 = plt.subplots(1, figsize = (19,9.5))
        sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')

        plt.scatter(np.array(self.test_fil["COP"]),COP_pred, c = self.test_fil["PLR"], cmap='jet', label = "COP_model")
        plt.plot([0, 10], [0, 10], "k--", label = "Bisector")
        plt.plot([0, 10], [0, 12], "k--", label = "Error +20%")                    
        plt.text( 6, 4.5, "-20%")
        plt.plot([0, 10], [0, 8], "k--", label = "Error -20%")
        plt.text( 6, 7.7, "+20%")
        cbar = plt.colorbar()
        cbar.set_label("PLR")
        plt.xlabel("Power_exp [kW]")
        plt.xlim(0,4)
        plt.ylim(0,4)
        plt.ylabel('Power_model[kW]')
        plt.legend()
        
        # plt.tight_layout()
        plt.savefig(os.path.join('..',"Results",f"{self.name}","New_models",f"NEW_MODEL_{status}.png"))
        plt.close()    
        
#%% Plot temporal pattern
    def plot_test(self,start_date,end_date):
        figure1, axs1 = plt.subplots(1,figsize = (19,9.5))
        sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
        font = 15
        
        self.test['Time'] = pd.to_datetime(self.test['Time'], unit='s')    
        filtered_data = self.test.loc[self.test["Time"] >= start_date]
        filtered_data = filtered_data.loc[filtered_data["Time"] <= end_date]
        x_data = np.array(filtered_data["Time"]) - pd.Timedelta(minutes = 2.5)
        
        #Method to color 
        def plot_state_as_color(x_data, state_data, axis, add_labels=True):
            state_current = state_data[0]
            span_left = x_data[0]
            state_encountered = []
            for span_right, state_next in zip(x_data, state_data):
                if state_current != state_next:
                    label = None
                    if state_current not in state_encountered:
                        state_encountered.append(state_current)
                        if add_labels:
                            label = state_current
                
                    # plot section
                    color = "C{}".format(state_encountered.index(state_current))
                    axis.axvspan(span_left, span_right, color=color, alpha=0.3, label=label)
                
                    # Update current state parameters
                    span_left = span_right
                    state_current = state_next    
            
            label = None
            if state_current not in state_encountered:
                state_encountered.append(state_current)
                if add_labels:
                    label = state_current
            color = "C{}".format(state_encountered.index(state_current))
            axis.axvspan(span_left, x_data[-1], color=color, alpha=0.3, label=label)
        
        axs1.plot(np.array(filtered_data["Time"]) ,np.array(filtered_data["Heat Cap COND [kW]"]), label = "Heat capacity [kW]")
        axs1.plot(np.array(filtered_data["Time"]),np.array(filtered_data["Pow [kW]"]), label = "Power [kW]")
        axs1.set_xlabel("Time [hours]",fontsize = font)
        axs1.tick_params(axis='y', labelsize= font)
        axs1.tick_params(axis='x', labelsize= font)
        axs1.set_ylabel("Power and HC [kW]",fontsize = font)
        plot_state_as_color(x_data, state_data=np.array(filtered_data["Status"]), axis=axs1)
        
        axs2 = axs1.twinx() 
        axs2.plot(np.array(filtered_data["Time"]), np.array(filtered_data["LExT [°C]"]), label = "LExT [°C]", color = "red")
        axs2.plot(np.array(filtered_data["Time"]),np.array(filtered_data["LET [°C]"]), label = "LET [°C]", color = "green")
        axs2.plot(np.array(filtered_data["Time"]),np.array(filtered_data["SET [°C]"]), label = "SET [°C]", color = "blue")
     
        axs1.legend(fontsize = font)
        axs2.legend(fontsize = font)

        plt.tight_layout()
        
#%% Err plot    
    def Err_Power(self,Pow_pred,status):
        
        #Create folder
        if not os.path.exists(os.path.join('..',"Results",self.name)):
            os.mkdir(os.path.join('..',"Results",self.name))
        else:
            pass
        
        if not os.path.exists(os.path.join('..',"Results",f"{self.name}","New_models")):
            os.mkdir(os.path.join('..',"Results",self.name,"New_models"))
        else:
            pass


        #Plot Power_pred vs residuals
        figure3, axs3 = plt.subplots(1, figsize = (19,9.5))
        sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
        residuals = Pow_pred - self.test_fil["Pow [kW]"]
        
        plt.scatter(np.array(self.test_fil["Pow [kW]"]),residuals, c = self.test_fil["PLR"], cmap='jet', label = "COP_model")
        cbar = plt.colorbar()
        cbar.set_label("PLR")
        plt.xlabel("Power_exp [kW]")
        plt.ylabel('Resiudals')
        plt.legend()
        
        # plt.tight_layout()
        plt.savefig(os.path.join('..',"Results",f"{self.name}","New_models",f"Error_{status}.png"))
        plt.close() 
        
#%%Full load plot    
    def plot_full_load(self):
        
        #Plot Power_pred vs Power_real 
        figure3, axs3 = plt.subplots(1,2, figsize = (19,9.5))
        df = self.test.loc[self.test["PLR"] >= 0.95]
        
        axs3[0].scatter(np.array(df["LExT [°C]"] - df["SET [°C]"]),np.array(df["Heat Cap COND [kW]"]),c = "blue")
        axs3[1].scatter(np.array(df["LExT [°C]"] - df["SET [°C]"]),np.array(df["Pow [kW]"]) ,c = "red")                
        axs3[0].set_xlabel("DeltaT")
        axs3[0].set_ylabel("HC full [kW]")
        axs3[1].set_xlabel("DeltaT")
        axs3[1].set_ylabel("Pow [kW]")
        
        plt.tight_layout()
        
#%%Rnvelope plot        
    def envelope_plot(self):
        
        #Create folder
        if not os.path.exists(os.path.join('..',"Results",self.name)):
            os.mkdir(os.path.join('..',"Results",self.name))
        else:
            pass
        
        if not os.path.exists(os.path.join('..',"Results",f"{self.name}","New_models")):
            os.mkdir(os.path.join('..',"Results",self.name,"New_models"))
        else:
            pass
        
        if np.max(self.train["LExT [°C]"]) == np.min(self.train["LExT [°C]"]):
            self.test = self.test.loc[(self.test["LExT [°C]"] <= np.max(self.train["LExT [°C]"])+ 5) & (self.test["LExT [°C]"] >= np.min(self.train["LExT [°C]"])- 5)]
        else:
            self.test = self.test_fil.loc[(self.test["LExT [°C]"] <= np.max(self.train["LExT [°C]"])) & (self.test["LExT [°C]"] >= np.min(self.train["LExT [°C]"]))]
        self.test = self.test.loc[(self.test["SET [°C]"] <= np.max(self.train["SET [°C]"])) & (self.test["SET [°C]"] >= np.min(self.train["SET [°C]"]))]
        
        #Plot Power_pred vs Power_real 
        figure1, axs1 = plt.subplots(1, figsize = (19,9.5))
        
        
        axs1.scatter(np.array(self.test["LExT [°C]"]),np.array(self.test["SET [°C]"]) ,c = "orange", alpha = 0.5)  
        axs1.scatter(np.array(self.train["LExT [°C]"]),np.array(self.train["SET [°C]"]),c = "blue",alpha = 0.5)              
        axs1.set_xlabel("LExT [°C]")
        axs1.set_ylabel("SET [°C]")
        axs1.set_xlabel("LExT [°C]")
        axs1.set_ylabel("SET [°C]")
    
        plt.tight_layout()    
        plt.savefig(os.path.join('..',"Results",f"{self.name}","New_models",f"Envelope_plot.png"))
        plt.close()   
#%%Funtion plot for ML
        
    def function_plot(self,font):

        
        #Create folder
        if not os.path.exists(os.path.join('..',"Results",self.name)):
            os.mkdir(os.path.join('..',"Results",self.name))
        else:
            pass
        
        if not os.path.exists(os.path.join('..',"Results",f"{self.name}","New_models")):
            os.mkdir(os.path.join('..',"Results",self.name,"New_models"))
        else:
            pass
        
        #Plot Power_pred vs Power_real 
        figure3, axs3 = plt.subplots(1,2, figsize = (19,9.5))
        sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
        
        #Testing points - fixed DeltaT 
        PLR = np.arange(0,1.1,0.01)
        Delta1 = np.full(len(PLR),30)
        Delta2 = np.full(len(PLR),40)
        Delta3 = np.full(len(PLR),50)
        Delta4 = np.full(len(PLR),60)
        
        X_train1 = np.column_stack((PLR,PLR/Delta1))
        X_train2 = np.column_stack((PLR,PLR/Delta2))
        X_train3 = np.column_stack((PLR,PLR/Delta3))
        X_train4 = np.column_stack((PLR,PLR/Delta4))

        
        #Model Calculation - No ML
        Y_test1 = self.model_reg_P.predict(X_train1)
        Y_test2 = self.model_reg_P.predict(X_train2)
        Y_test3 = self.model_reg_P.predict(X_train3)
        Y_test4 = self.model_reg_P.predict(X_train4)

        
        #Model Calculation - ML
        Y_test1_ML = self.model_reg_P_ML.predict(X_train1)
        Y_test2_ML = self.model_reg_P_ML.predict(X_train2)
        Y_test3_ML = self.model_reg_P_ML.predict(X_train3)
        Y_test4_ML = self.model_reg_P_ML.predict(X_train4)

        
        #Plot creation
        axs3[0].plot(PLR,Y_test1,c = "blue",label = "DeltaT = 30 K",linewidth=2.0)
        axs3[0].plot(PLR,Y_test2,c = "orange",label = "DeltaT = 40 K",linewidth=2.0)
        axs3[0].plot(PLR,Y_test3,c = "green",label = "DeltaT = 50 K",linewidth=2.0)
        axs3[0].plot(PLR,Y_test4,c = "purple",label = "DeltaT = 60 K",linewidth=2.0)
       
        axs3[0].set_xlabel("PLR", fontsize = font)
        axs3[0].set_xlim(0.2,1)
        axs3[0].set_ylim(0,1)
        axs3[0].set_ylabel("$Y_{Catalogue}$", fontsize = font)
        axs3[0].tick_params(axis='both', labelsize= font)
        axs3[0].legend(fontsize = font)
        
        axs3[1].plot(PLR, Y_test1_ML,c = "blue",label = "DeltaT = 30 K",linewidth=2.0)
        axs3[1].plot(PLR, Y_test2_ML,c = "orange",label = "DeltaT = 40 K",linewidth=2.0)
        axs3[1].plot(PLR, Y_test3_ML,c = "green",label = "DeltaT = 50 K",linewidth=2.0)
        axs3[1].plot(PLR, Y_test4_ML,c = "purple",label = "DeltaT = 60 K",linewidth=2.0)
        
        axs3[1].set_xlabel("PLR", fontsize = font)
        axs3[1].set_xlim(0.2,1)
        axs3[1].set_ylim(0,1)
        axs3[1].tick_params(axis='both', labelsize= font)
        axs3[1].set_ylabel("$Y_{Experimental}$",fontsize = font)
        
    
        figure3.suptitle("Linear regression on Catalogues vs Experimental",fontsize = font)
        plt.tight_layout()
        plt.savefig(os.path.join('..',"Results",f"{self.name}","New_models",f"Function_plot.png"))
        plt.close()

    def function_plot_2(self,font):
        
        #Create folder
        if not os.path.exists(os.path.join('..',"Results",self.name)):
            os.mkdir(os.path.join('..',"Results",self.name))
        else:
            pass
        
        if not os.path.exists(os.path.join('..',"Results",f"{self.name}","New_models")):
            os.mkdir(os.path.join('..',"Results",self.name,"New_models"))
        else:
            pass
        
        #Plot Power_pred vs Power_real 
        figure3, axs3 = plt.subplots(1,2, figsize = (19,9.5))
        sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
        
        #Testing points - fixed PLR
        DeltaT = np.arange(10,50,0.01)
        PLR1 = np.full(len(DeltaT),0.2)
        PLR2 = np.full(len(DeltaT),0.4)
        PLR3 = np.full(len(DeltaT),0.6)
        PLR4 = np.full(len(DeltaT),0.8)
        PLR5 = np.full(len(DeltaT),1)

        
        X_train1 = np.column_stack((PLR1,PLR1/DeltaT))
        X_train2 = np.column_stack((PLR2,PLR2/DeltaT))
        X_train3 = np.column_stack((PLR3,PLR3/DeltaT))
        X_train4 = np.column_stack((PLR4,PLR4/DeltaT))
        X_train5 = np.column_stack((PLR5,PLR5/DeltaT))
        
        
        #Model Calculation - No ML
        Y_test1 = self.model_reg_P.predict(X_train1)
        Y_test2 = self.model_reg_P.predict(X_train2)
        Y_test3 = self.model_reg_P.predict(X_train3)
        Y_test4 = self.model_reg_P.predict(X_train4)
        Y_test5 = self.model_reg_P.predict(X_train5)
  
        
        #Model Calculation - ML
        Y_test1_ML = self.model_reg_P_ML.predict(X_train1)
        Y_test2_ML = self.model_reg_P_ML.predict(X_train2)
        Y_test3_ML = self.model_reg_P_ML.predict(X_train3)
        Y_test4_ML = self.model_reg_P_ML.predict(X_train4)
        Y_test5_ML = self.model_reg_P_ML.predict(X_train5)
        
        
        #Plot creation
        axs3[0].plot(DeltaT,Y_test1,c = "blue",label = "PLR = 20% ",linewidth=2.0)
        axs3[0].plot(DeltaT,Y_test2,c = "orange",label = "PLR = 40% ",linewidth=2.0)
        axs3[0].plot(DeltaT,Y_test3,c = "green",label = "PLR = 60% ",linewidth=2.0)
        axs3[0].plot(DeltaT,Y_test4,c = "purple",label = "PLR = 80% ",linewidth=2.0)
        axs3[0].plot(DeltaT,Y_test5,c = "grey",label = "PLR = 100% ",linewidth=2.0)
       
        axs3[0].set_xlabel("DeltaT", fontsize = font)
        axs3[0].set_xlim(10,50)
        axs3[0].set_ylim(0,1)
        axs3[0].set_ylabel("$Y_{Catalogue}$", fontsize = font)
        axs3[0].tick_params(axis='both', labelsize= font)
        axs3[0].legend(fontsize = font)
        
        axs3[1].plot(DeltaT, Y_test1_ML,c = "blue",label = "PLR = 20% ",linewidth=2.0)
        axs3[1].plot(DeltaT, Y_test2_ML,c = "orange",label = "PLR = 40% ",linewidth=2.0)
        axs3[1].plot(DeltaT, Y_test3_ML,c = "green",label = "PLR = 60% ",linewidth=2.0)
        axs3[1].plot(DeltaT, Y_test4_ML,c = "purple",label = "PLR = 80% ",linewidth=2.0)
        axs3[1].plot(DeltaT, Y_test5_ML,c = "grey",label = "PLR = 100% ",linewidth=2.0)
      
        axs3[1].set_xlabel("DeltaT", fontsize = font)
        axs3[1].set_xlim(10,50)
        axs3[1].set_ylim(0,1)
        axs3[1].tick_params(axis='both', labelsize= font)
        axs3[1].set_ylabel("$Y_{Experimental}$",fontsize = font)
        
    
        figure3.suptitle("Linear regression on Catalogues vs Experimental",fontsize = font)
        plt.tight_layout()
        plt.savefig(os.path.join('..',"Results",f"{self.name}","New_models",f"Function_plot_PLRcost.png"))
        plt.close()

    # def plt_hist(self):
    #     df = self.test.loc[self.test["Status"] != "OFF"]
    #     df.plot.hist(column = ["LExT [°C]"],bins = 10)
    #     print(df["LExT [°C]"].quantile(q=0.1))
    #     print(df["LExT [°C]"].quantile(q=0.9))

#%% Exp power ratio plot
    
    def plot_power_ratio(self):
        figure1, axs1 = plt.subplots(1,2, figsize = (19,9.5))
        figure2, axs2 = plt.subplots(1,2, figsize = (19,9.5))
        
        pow_ratio = self.test_stat["Pow [kW]"]/self.test_stat["Pow full [kW]"]
        pow_ratio_pred = self.test_stat["Pow_pred"]/self.test_stat["Pow full [kW]"]
        
        pow_ratio_mod = self.test_mod["Pow [kW]"]/self.test_mod["Pow full [kW]"]
        pow_ratio_mod_pred = self.test_mod["Pow_pred"]/self.test_mod["Pow full [kW]"]
        
        delta = self.test_stat["LExT [°C]"] - self.test_stat["SET [°C]"]
        delta_MOD = self.test_mod["LExT [°C]"] - self.test_mod["SET [°C]"]

        delta_scal = (delta - min(delta))/(max(delta) - min(delta))
        delta_scal_mod = (delta_MOD - min(delta_MOD))/(max(delta_MOD) - min(delta_MOD))
        
        axs1[0].scatter(np.array(self.test_stat["PLR"]),self.test_stat["Pow_ratio"], c = "blue")
        axs1[0].scatter(np.array(self.test_stat["PLR"]),pow_ratio_pred, c = "orange")
        axs1[1].scatter(np.array(self.test_mod["PLR"]),self.test_mod["Pow_ratio"], c = "blue")
        axs1[1].scatter(np.array(self.test_mod["PLR"]),pow_ratio_mod_pred, c = "orange")
  
        axs2[0].scatter(np.array(delta_scal),self.test_stat["Pow_ratio"], c = "blue")
        axs2[0].scatter(np.array(delta_scal),pow_ratio_pred, c = "orange")
        axs2[1].scatter(np.array(delta_scal_mod),self.test_mod["Pow_ratio"], c = "blue")
        axs2[1].scatter(np.array(delta_scal_mod),pow_ratio_mod_pred, c = "orange")
        plt.show()
        
#%% Methods in the HPs classes
    #Method to analalise the status of operation of the HP    
    def status_analysis(self):
        
        #Find Power and HC in design conditions
        self.SET_des = -7
        self.LExT_des = 35
        
        try:
            self.Pow_des = self.train_fl.loc[(self.train_fl["SET [°C]"] == self.SET_des) & (self.train_fl["LExT [°C]"] ==  self.LExT_des),"Pow [kW]"].item()
            self.HC_des = self.train_fl.loc[(self.train_fl["SET [°C]"] ==  self.SET_des) & (self.train_fl["LExT [°C]"] ==  self.LExT_des),'Heat Cap COND [kW]'].item()
        
        except ValueError:
            
            self.SET_des = self.train_fl.loc[self.train_fl.index == 0, "SET [°C]"].item()
            self.LExT_des = self.train_fl.loc[self.train_fl.index == 0, "LExT [°C]"].item()
            
            self.Pow_des = self.train_fl.loc[self.train_fl.index == 0, "Pow [kW]"].item()
            self.HC_des = self.train_fl.loc[self.train_fl.index == 0, "Heat Cap COND [kW]"].item()
            
        #Clean the dataset
        col = ["Time","Pow [kW]","Heat Cap COND [kW]", "LExT [°C]", "LET [°C]","SET [°C]"]
        self.test.columns = col
       
        #Ground source heat pumps
        if self.source == "WtW":
            mean_air_t = np.mean(self.test["SET [°C]"])
            #Set costant soil temperature at around 50 m of depht of the borehole, increaed by 1.5 °C
            self.test["SET [°C]"] = np.full(len(self.test["Time"]),1.5 + mean_air_t)

        
        #Conversion units of measurement
        self.test['Heat Cap COND [kW]'] = self.test['Heat Cap COND [kW]']/1000 #trasform to kW
        self.test['Pow [kW]'] = self.test['Pow [kW]']/1000  #trasform to kW
        self.test = self.test.reset_index()
        
        #Initilize status
        status = []
        
        #ON-OFF status
        p_thresh = 0.05*self.Pow_des #[kW] 5% of the full load power SET =-7°C and LExT = 35°C from catalogue
        for i in self.test.index:
            if self.test["Pow [kW]"].get(i) < p_thresh:
                status.append('OFF')
            else:
                status.append(0)
                
        #Define Gradient
        #Values equally spaced by a 5 minutes interval
        x_min = np.zeros(len(self.test["Time"]))
        
        for i in self.test.index:
            x_min[i] = (self.test.loc[i,"Time"] - self.test.loc[0,"Time"]).total_seconds() /60
        
        Grad_HC = np.gradient(self.test["Heat Cap COND [kW]"],x_min)  #compute the gradient using the delta time of 5 minutes [kW/min]
        
        #Try usign savgol_filter
        # Grad_HC = savgol_filter(self.test["Heat Cap COND [kW]"], window_length=7, polyorder=3, deriv=1, delta=5)
        
        #START and STOP status
        for i in self.test.index:
            if status[i] == 0 and status[i-1] == 'OFF':
                status[i] = 'START'
            elif status[i] == 'OFF' and status[i-1] == 0:
                status[i] = 'STOP'
                
        #DHW and DEF Status
        DeltaT = self.test["LExT [°C]"] - self.test["LET [°C]"]
        for i in self.test.index:
            if self.test["LExT [°C]"].get(i) > 50: #Above 50°C the unit is producing DHW
                status[i] = 'DHW'
            
            #Defrost just for AtW or AtA HPs
            if self.source == "AtW" or self.source == "AtA":
                if (DeltaT[i] < 1 and status[i] == 0) or (self.test["Heat Cap COND [kW]"].get(i) <0 and status[i] == 0):
                    status[i] = 'DEF'
                
        #Modulation and steady state regime - AtW
        if self.source == "AtW" or self.source == "AtA":
            for i in self.test.index:
                if status[i] == 0 and abs(Grad_HC[i]) <= 0.05 * self.HC_des:
                    status[i] = 'STATIONARY'
                elif status[i] == 0 and Grad_HC[i] > 0.05 * self.HC_des:
                    status[i] = 'ACCELERATION'
                elif status[i] == 0 and Grad_HC[i] < -0.05 * self.HC_des: #kW/min
                    status[i] = 'DECELERATION'
        
        #Modulation and steady state regime - WtW
        #Since the units with water have a greater inertia, a smaller limit is required.
        if self.source == "WtW"or self.source == "WtA":
            for i in self.test.index:
                if status[i] == 0 and abs(Grad_HC[i]) <= 0.05 * self.HC_des:
                    #10%  of the full load HC SET =-7°C and LExT = 35°C from catalogue
                    status[i] = 'STATIONARY'
                elif status[i] == 0 and Grad_HC[i] > 0.005* self.HC_des:
                    status[i] = 'ACCELERATION'
                elif status[i] == 0 and Grad_HC[i] < -0.005 * self.HC_des: #kW/min
                    status[i] = 'DECELERATION'     
        
        self.test["Status"] = status
                
        #Clean power absortion (error of measuremnt)
        #Set boundary at 8 kW
        self.test = self.test.loc[self.test["Pow [kW]"] <= 8]
        
        return self.test        
    
#%% #Full load intrerpolation calculation
    def interp_full_load(self):
 
            
        #Drop Nan values
        self.test = self.test[self.test["Pow [kW]"] != 0]
        self.test = self.test[self.test['Pow [kW]'].notna()]
        self.test = self.test[self.test['Heat Cap COND [kW]'].notna()]
        self.test = self.test[self.test['LExT [°C]'].notna()]
        self.test = self.test[self.test['LET [°C]'].notna()]
        self.test = self.test[self.test["SET [°C]"].notna()]
        # self.test = self.test[test["LFR [kg/s]"].notna()]
        
        
        #Get data train - First Training
        SET = np.array(self.train_fl["SET [°C]"] + 273.15)
        SET_des = self.SET_des + 273.15  #Trasform to K
        LExT = np.array(self.train_fl["LExT [°C]"] + 273.15)
        LExT_des = self.LExT_des + 273.15 #Trasform to K
        Delta1 = (LExT - SET)/(LExT_des - SET_des)
        Delta2 = Delta1**2
        
        #Get data test
        SET_exp = np.array(self.test["SET [°C]"] + 273.15)
        LExT_exp = np.array(self.test["LExT [°C]"] + 273.15)
        Delta1_exp = (LExT_exp - SET_exp)/(LExT_des - SET_des)
        Delta2_exp = np.array(Delta1_exp**2)
         
        #Create train and test model
        X_train_HC = np.array(Delta1)
        Y_train_HC =  np.array(self.train_fl['Heat Cap COND [kW]']/self.HC_des)
        X_test_HC = np.array(Delta1_exp)
                             
        # X_train_HC = np.column_stack((Delta1,Delta2))
        # Y_train_HC =  np.array(self.train_fl['Heat Cap COND [kW]']/self.HC_des)
        # X_test_HC = np.column_stack((Delta1_exp,Delta2_exp))
        
        X_train_Pow = np.array(Delta1)
        Y_train_Pow =  np.array(self.train_fl['Pow [kW]']/self.Pow_des)
        X_test_Pow = np.array(Delta1_exp)
        
        # X_train_Pow = np.column_stack((Delta1,Delta2))
        # Y_train_Pow =  np.array(self.train_fl['Pow [kW]']/self.Pow_des)
        # X_test_Pow = np.column_stack((Delta1_exp,Delta2_exp))

        
        #Linear model and evalutaion of residuals
        X_train_HC = sm.add_constant(X_train_HC)
        ols_model_HC = sm.OLS(Y_train_HC,X_train_HC).fit()
        residuals_HC = ols_model_HC.resid
        residuals_HC_2 =  residuals_HC **2
           
        
        #Linear model and evaluation of residuals
        X_train_Pow = sm.add_constant(X_train_Pow)
        ols_model_Pow = sm.OLS(Y_train_Pow,X_train_Pow).fit()
        residuals_Pow = ols_model_Pow.resid
        residuals_Pow_2 = residuals_Pow**2
           
        #Append to train   
        self.train_fl["Weights_HC"] = 1/abs(residuals_HC)
        self.train_fl["Weights_Pow"] = 1 /abs(residuals_Pow)  

        
        #Second Training - HC
        X_train_HC = sm.add_constant(X_train_HC)
        model_HC_weight = sm.WLS(Y_train_HC, X_train_HC, weights= self.train_fl["Weights_HC"])
        model_HC_weight = model_HC_weight.fit()
        
        #Calculate the HC Full Load
        X_test_HC = sm.add_constant(X_test_HC)
        HC_fl_model_weight = model_HC_weight.predict(X_test_HC)*self.HC_des
        
        #Second Training - Power
        X_train_Pow = sm.add_constant(X_train_Pow)
        model_Pow_weight = sm.WLS(Y_train_Pow, X_train_Pow, weights= self.train_fl["Weights_Pow"])
        model_Pow_weight = model_Pow_weight.fit()

        #Calculate the Power Consuption Full Load
        X_test_Pow = sm.add_constant(X_test_Pow)
        Pow_fl_model_weight = model_Pow_weight.predict(X_test_Pow)*self.Pow_des

        #Create dataframe
        PLR = self.test['Heat Cap COND [kW]']/HC_fl_model_weight
        self.test['PLR'] = PLR
        self.test["COP"] = self.test["Heat Cap COND [kW]"]/self.test["Pow [kW]"]
        self.test["Heat Cap COND full [kW]"] = HC_fl_model_weight
        self.test["Pow full [kW]"] = Pow_fl_model_weight
        self.test["Pow_ratio"] = self.test["Pow [kW]"]/ Pow_fl_model_weight
        
        #Adjust PLR
        # for i in self.test.index.values:
        #     if self.test.loc[i,"PLR"] > 1:
        #         self.test.loc[i,"PLR"] = 1
        #     elif self.test.loc[i,"PLR"] < 0:
        #         self.test.loc[i,"PLR"] = 0
        
        # #Adjust POW - no values greater than 1
        # for i in self.test.index.values:
        #     if self.test.loc[i,"Pow_ratio"] > 1:
        #         self.test.loc[i,"Pow_ratio"] = 1
        #     elif self.test.loc[i,"Pow_ratio"] < 0:
        #         self.test.loc[i,"Pow_ratio"] = 0
        
        #Cleaning from outlayers the X variable PLR
        mean = self.test["PLR"].mean()
        std = self.test["PLR"].std()
        
        self.test =self.test[(self.test["PLR"] >= mean - 3*std) &
                    (self.test["PLR"] <= mean + 3*std)]
        
        #Cleaning from outlayers the target Y
        mean = self.test["Pow_ratio"].mean()
        std = self.test["Pow_ratio"].std()
        
        self.test =self.test[(self.test["Pow_ratio"] >= mean - 3*std) &
                    (self.test["Pow_ratio"] <= mean + 3*std)]
        
        return self.test  
                    
#%%Select best features
    def Selectbest(self):
        X = np.column_stack((self.test["PLR"],self.test["LExT [°C]"],self.test["SET [°C]"],self.test["LExT [°C]"] -self.test["SET [°C]"]))
        Y = self.test["Pow [kW]"]/self.test["Pow full [kW]"]
    
        selector = SelectKBest(score_func=f_regression, k=2)
        X_new = selector.fit_transform(X, Y)
        
        mask = selector.get_support()
        selected_features =[i for i, x in enumerate(mask) if x]
    
        print("Migliori feature:", selected_features)
        
        #Correlation -stat
        # fil = self.test.loc[self.test['Status'] == "STATIONARY"]
        fil = self.test.loc[(self.test['Status'] == 'ACCELERATION') | (self.test['Status'] == 'DECELERATION')]
                  
        df = fil.loc[:,["Pow_ratio","PLR"]]
        df["sqrt PLR"] = np.sqrt(df["PLR"])
        df["inv PLR"] = 1/df["PLR"]
        df["log PLR"] = np.log(df["PLR"])
        df["Delta"] = fil["LExT [°C]"] -fil["SET [°C]"]
        Pears = df.corr("pearson")
        Spear = df.corr("spearman")
        
        
        return (Pears,Spear,df)
#%%#Calculation of the model KPIs and Results
    def new_model_fit(self):        

        self.KPI = {}
        col = ["R2_Pow","MAPE_Pow","RMSE_Pow",
               "MAPE_COP","RMSE_COP",
               "SCOP_model","SCOP_exp","Err_SCOP [%]"]
        
        states = ["STATIONARY","MODULATION","MOD + DEF","ALL"]
        multindex = [[self.name],states]
        multindex = pd.MultiIndex.from_product(multindex, names = ["model","status"])
        self.KPI = pd.DataFrame(self.KPI,index = multindex,columns = col)
                    
        #Filter on PLR
        # self.test_fil = self.test_fil.loc[self.test_fil["PLR"] <= 0.8]
        # self.train = self.train.loc[self.train["PLR"] <= 0.8]
        
        
        # #Filter on training data -LExT and SET
        # if np.max(self.train["LExT [°C]"]) == np.min(self.train["LExT [°C]"]):
        #     self.test_fil = self.test_fil.loc[(self.test_fil["LExT [°C]"] <= np.max(self.train["LExT [°C]"])+ 5) & (self.test_fil["LExT [°C]"] >= np.min(self.train["LExT [°C]"])- 5)]
        # else:
        #     self.test_fil = self.test_fil.loc[(self.test_fil["LExT [°C]"] <= np.max(self.train["LExT [°C]"])) & (self.test_fil["LExT [°C]"] >= np.min(self.train["LExT [°C]"]))]
        # self.test_fil = self.test_fil.loc[(self.test_fil["SET [°C]"] <= np.max(self.train["SET [°C]"])) & (self.test_fil["SET [°C]"] >= np.min(self.train["SET [°C]"]))]
        
        #Separate the dataset
        self.test_stat = self.test.loc[self.test["Status"] == "STATIONARY"]
        self.test_mod = self.test.loc[(self.test['Status'] == 'ACCELERATION') | (self.test['Status'] == 'DECELERATION')]
                   # | (self.test['Status'] == 'START') | (self.test['Status'] == 'STOP')]
        
        #Normalize the thermodynamics variables - Catalogue
        Delta1 = self.train["LExT [°C]"]-self.train["SET [°C]"]
        scal_D = (Delta1 - min(Delta1))/(max(Delta1)- min(Delta1))
        PLR =  self.train["PLR"]
    
         # #Normalize the thermodinamics variables - STAT
        Delta1_exp = self.test_stat["LExT [°C]"]-self.test_stat["SET [°C]"]
        scal_D_exp = (Delta1_exp - min(Delta1_exp))/(max(Delta1_exp)- min(Delta1_exp))
        PLR_exp =  self.test_stat["PLR"]
        
        # #Normalize the thermodinamics variables - mod
        Delta1_exp_m = self.test_mod["LExT [°C]"]-self.test_mod["SET [°C]"]
        PLR_exp_m =  self.test_mod["PLR"]
                
        
         # Model input STAT
        X_train = np.column_stack((PLR,PLR*scal_D))
        X_test = np.column_stack((PLR_exp, PLR_exp*scal_D_exp))
        Y_train = self.train["Pow [kW]"]/self.train["Pow full [kW]"]
        
        #Model input modulation
        X_train_mod = PLR.values.reshape(-1,1)
        X_test_mod = PLR_exp_m.values.reshape(-1,1)

        # Model regression_ stationary
        self.model_reg_P = linear_model.LinearRegression(fit_intercept = True).fit(X_train, Y_train)
        Pow_pred =  self.model_reg_P.predict(X_test)* self.test_stat["Pow full [kW]"]
        residuals = abs(Pow_pred - self.test_stat["Pow [kW]"])
        self.test_stat = self.test_stat.copy()
        self.test_stat["Residuals"] = residuals
        self.test_stat["Pow_pred"] = Pow_pred
        
        # Model regression_ modulation
        self.model_reg_P_mod = linear_model.LinearRegression(fit_intercept = True).fit(X_train_mod, Y_train)
        Pow_pred_mod =  self.model_reg_P_mod.predict(X_test_mod)* self.test_mod["Pow full [kW]"]
        residuals = abs(Pow_pred_mod - self.test_mod["Pow [kW]"])
        self.test_mod = self.test_mod.copy()
        self.test_mod["Residuals"] = residuals
        self.test_mod["Pow_pred"] = Pow_pred_mod
        
        
        #Outlayers detection and elimination - Assumed a maximum residual of 100 kW 
        self.test_stat = self.test_stat.loc[self.test_stat["Residuals"] < 100]
        self.test_mod = self.test_mod.loc[self.test_mod["Residuals"] < 100]
        
        # #COP calculation
        # COP_pred = self.test_stat["Heat Cap COND [kW]"]/self.test_stat["Pow_pred"]
        # COP_pred.replace([np.inf, -np.inf], np.nan, inplace=True)
        # COP_pred.fillna(0, inplace = True)
        
        #SCOP calculation
        SCOP_model_stat = sum(np.array(self.test_stat["Heat Cap COND [kW]"]))/sum(self.test_stat["Pow_pred"])
        SCOP_exp_stat= sum(np.array(self.test_stat["Heat Cap COND [kW]"]))/sum(np.array(self.test_stat["Pow [kW]"]))
        SCOP_model_mod = sum(np.array(self.test_mod["Heat Cap COND [kW]"]))/sum(self.test_mod["Pow_pred"])
        SCOP_exp_mod= sum(np.array(self.test_mod["Heat Cap COND [kW]"]))/sum(np.array(self.test_mod["Pow [kW]"]))
        
        #KPI Calculations 

        self.KPI.loc[(self.name,"STATIONARY"),"R2_Pow"] = float(r2_score(self.test_stat["Pow [kW]"],self.test_stat["Pow_pred"]))
        self.KPI.loc[(self.name,"STATIONARY"),"MAPE_Pow"] = float(mean_absolute_percentage_error(self.test_stat["Pow [kW]"],self.test_stat["Pow_pred"]))
        self.KPI.loc[(self.name,"STATIONARY"),"RMSE_Pow"] = float(root_mean_squared_error(self.test_stat["Pow [kW]"],self.test_stat["Pow_pred"]).astype(float))
         
           
         #SCOP
        self.KPI.loc[(self.name,"STATIONARY"),"SCOP_model"] = float(SCOP_model_stat.astype(float))
        self.KPI.loc[(self.name,"STATIONARY"),"SCOP_exp"] = float(SCOP_exp_stat.astype(float))
        self.KPI.loc[(self.name,"STATIONARY"),"Err_SCOP [%]"] = float((SCOP_model_stat - SCOP_exp_stat)/SCOP_exp_stat *100)
         

        self.KPI.loc[(self.name,"ALL"),"R2_Pow"] = float(r2_score(self.test_mod["Pow [kW]"],self.test_mod["Pow_pred"]))
        self.KPI.loc[(self.name,"ALL"),"MAPE_Pow"] = float(mean_absolute_percentage_error(self.test_mod["Pow [kW]"],self.test_mod["Pow_pred"]))
        self.KPI.loc[(self.name,"ALL"),"RMSE_Pow"] = float(root_mean_squared_error(self.test_mod["Pow [kW]"],self.test_mod["Pow_pred"]).astype(float))
         
         #SCOP
        self.KPI.loc[(self.name,"ALL"),"SCOP_model"] = float(SCOP_model_mod.astype(float))
        self.KPI.loc[(self.name,"ALL"),"SCOP_exp"] = float(SCOP_exp_mod.astype(float))
        self.KPI.loc[(self.name,"ALL"),"Err_SCOP [%]"] = float((SCOP_model_mod - SCOP_exp_mod)/SCOP_exp_mod *100)
           
                
        return self.KPI

#%% Calculation of the model KPIs and Results usign ML Approach
    def new_model_fit_ML(self):        

        self.KPI_ML = {}
        
        col = ["R2_Pow","MAPE_Pow","RMSE_Pow",
               "MAPE_COP","RMSE_COP",
               "SCOP_model","SCOP_exp","Err_SCOP [%]"]
        
        states = ["STATIONARY","MODULATION","MOD + DEF","ALL"]
        multindex = [[self.name],states]
        multindex = pd.MultiIndex.from_product(multindex, names = ["model","status"])
        self.KPI_ML = pd.DataFrame(self.KPI_ML,index = multindex,columns = col)
                    
        #Filter
        for i in range(4):
            if i == 0:
               self.test_fil = self.test[self.test['Status'] == 'STATIONARY']
            elif i == 1:
                self.test_fil = self.test[(self.test['Status'] == 'ACCELERATION') | (self.test['Status'] == 'DECELERATION')
                          | (self.test['Status'] == 'STATIONARY') | (self.test['Status'] == 'START') | (self.test['Status'] == 'STOP')]
            elif i == 2:
                self.test_fil = self.test[(self.test['Status'] == 'ACCELERATION') | (self.test['Status'] == 'DECELERATION') | (self.test['Status'] == 'START')
                         | (self.test['Status'] == 'STOP') | (self.test['Status'] == 'STATIONARY') | (self.test['Status'] == 'DEF')]
            elif i == 3:
                self.test_fil = self.test[(self.test['Status'] == 'ACCELERATION') | (self.test['Status'] == 'DECELERATION')| (self.test['Status'] == 'START') | (self.test['Status'] == 'STOP')
                          | (self.test['Status'] == 'STATIONARY') | (self.test['Status'] == 'DEF')  | (self.test['Status'] == 'DHW')]
            
           
            #Filter on PLR
            # self.test_fil = self.test_fil.loc[self.test_fil["PLR"] <= 0.8]
            # self.train = self.train.loc[self.train["PLR"] <= 0.8]
            
            #Normalize the thermodinamics variables - experimental Data
            Delta1_exp = self.test_fil["LExT [°C]"]-self.test_fil["SET [°C]"]
            PLR_exp =  self.test_fil["PLR"]
                    
            #Input
            X = np.column_stack((PLR_exp,PLR_exp/Delta1_exp, self.test_fil["Heat Cap COND [kW]"],self.test_fil["Pow [kW]"],self.test_fil["COP"]))
            Y = np.column_stack((self.test_fil["Pow [kW]"]/self.test_fil["Pow full [kW]"],self.test_fil["Pow full [kW]"]))
            
            #Control Approach
            X_train,X_test,Y_train,Y_test = train_test_split(X,Y, test_size = 0.2)
        
        
            #Linear regression model
            self.model_reg_P_ML = linear_model.LinearRegression(fit_intercept = True).fit(X_train[:,[0,1]], Y_train[:,0])
            # print(model_reg_P.coef_)
            Pow_pred =  self.model_reg_P_ML.predict(X_test[:,[0,1]])* Y_test[:,1]
            # Pow_pred = model_Pow_weight.predict(X_test)* Y_test["Pow full [kW]"]
            
            
            #COP calculation
            COP_pred = X_test[:,2]/Pow_pred
            COP_pred[np.isinf(COP_pred)] = 0
            # COP_pred.replace([np.inf, -np.inf], np.nan, inplace=True)
            # COP_pred.fillna(0, inplace = True)
            
            #SCOP calculation
            SCOP_model = sum( X_test[:,2])/sum(Pow_pred)
            SCOP_exp = sum( X_test[:,2])/sum(X_test[:,3])
            
            #KPI Calculations 
            if i == 0:
               self.KPI_ML.loc[(self.name,"STATIONARY"),"R2_Pow"] = float(r2_score(X_test[:,3],Pow_pred))
               self.KPI_ML.loc[(self.name,"STATIONARY"),"MAPE_Pow"] = float(mean_absolute_percentage_error(X_test[:,3],Pow_pred))
               self.KPI_ML.loc[(self.name,"STATIONARY"),"RMSE_Pow"] = float(root_mean_squared_error(X_test[:,3],Pow_pred).astype(float))
                
                # #COP
               self.KPI_ML.loc[(self.name,"STATIONARY"),"MAPE_COP"] = float(mean_absolute_percentage_error(X_test[:,4],COP_pred))
               self.KPI_ML.loc[(self.name,"STATIONARY"),"RMSE_COP"] = float(root_mean_squared_error(X_test[:,4],COP_pred).astype(float))
                  
                #SCOP
               self.KPI_ML.loc[(self.name,"STATIONARY"),"SCOP_model"] = float(SCOP_model.astype(float))
               self.KPI_ML.loc[(self.name,"STATIONARY"),"SCOP_exp"] = float(SCOP_exp.astype(float))
               self.KPI_ML.loc[(self.name,"STATIONARY"),"Err_SCOP [%]"] = float((SCOP_model - SCOP_exp)/SCOP_exp *100)

    
            elif i == 1:
               self.KPI_ML.loc[(self.name,"MODULATION"),"R2_Pow"] = float(r2_score(X_test[:,3],Pow_pred))
               self.KPI_ML.loc[(self.name,"MODULATION"),"MAPE_Pow"] = float(mean_absolute_percentage_error(X_test[:,3],Pow_pred))
               self.KPI_ML.loc[(self.name,"MODULATION"),"RMSE_Pow"] = float(root_mean_squared_error(X_test[:,3],Pow_pred).astype(float))
                
                #COP
               self.KPI_ML.loc[(self.name,"MODULATION"),"MAPE_COP"] = float(mean_absolute_percentage_error(X_test[:,4],COP_pred))
               self.KPI_ML.loc[(self.name,"MODULATION"),"RMSE_COP"] = float(root_mean_squared_error(X_test[:,4],COP_pred).astype(float))
                
                #SCOP
               self.KPI_ML.loc[(self.name,"MODULATION"),"SCOP_model"] = float(SCOP_model.astype(float))
               self.KPI_ML.loc[(self.name,"MODULATION"),"SCOP_exp"] = float(SCOP_exp.astype(float))
               self.KPI_ML.loc[(self.name,"MODULATION"),"Err_SCOP [%]"] = float((SCOP_model - SCOP_exp)/SCOP_exp *100)
                
            
            elif i == 2:
               self.KPI_ML.loc[(self.name,"MOD + DEF"),"R2_Pow"] = float(r2_score(X_test[:,3],Pow_pred))
               self.KPI_ML.loc[(self.name,"MOD + DEF"),"MAPE_Pow"] = float(mean_absolute_percentage_error(X_test[:,3],Pow_pred))
               self.KPI_ML.loc[(self.name,"MOD + DEF"),"RMSE_Pow"] = float(root_mean_squared_error(X_test[:,3],Pow_pred).astype(float))
                
                #COP
               self.KPI_ML.loc[(self.name,"MOD + DEF"),"MAPE_COP"] = float(mean_absolute_percentage_error(X_test[:,4],COP_pred))
               self.KPI_ML.loc[(self.name,"MOD + DEF"),"RMSE_COP"] = float(root_mean_squared_error(X_test[:,4],COP_pred).astype(float))
                
                #SCOP
               self.KPI_ML.loc[(self.name,"MOD + DEF"),"SCOP_model"] = float(SCOP_model.astype(float))
               self.KPI_ML.loc[(self.name,"MOD + DEF"),"SCOP_exp"] = float(SCOP_exp.astype(float))
               self.KPI_ML.loc[(self.name,"MOD + DEF"),"Err_SCOP [%]"] = float((SCOP_model - SCOP_exp)/SCOP_exp *100)
                
            elif i == 3:
               self.KPI_ML.loc[(self.name,"ALL"),"R2_Pow"] = float(r2_score(X_test[:,3],Pow_pred))
               self.KPI_ML.loc[(self.name,"ALL"),"MAPE_Pow"] = float(mean_absolute_percentage_error(X_test[:,3],Pow_pred))
               self.KPI_ML.loc[(self.name,"ALL"),"RMSE_Pow"] = float(root_mean_squared_error(X_test[:,3],Pow_pred).astype(float))
                
                #COP
               self.KPI_ML.loc[(self.name,"ALL"),"MAPE_COP"] = float(mean_absolute_percentage_error(X_test[:,4],COP_pred))
               self.KPI_ML.loc[(self.name,"ALL"),"RMSE_COP"] = float(root_mean_squared_error(X_test[:,4],COP_pred).astype(float))
                
                #SCOP
               self.KPI_ML.loc[(self.name,"ALL"),"SCOP_model"] = float(SCOP_model.astype(float))
               self.KPI_ML.loc[(self.name,"ALL"),"SCOP_exp"] = float(SCOP_exp.astype(float))
               self.KPI_ML.loc[(self.name,"ALL"),"Err_SCOP [%]"] = float((SCOP_model - SCOP_exp)/SCOP_exp *100)
                
        return self.KPI_ML

#%% New class for comparing different heat pumps   
     
class Heat_Pumps_comparison():
    
    
    def __init__(self,HP1, HP2):
        self.HP1 = HP1
        self.HP2 = HP2
        
    def test_on_different_machines(self):
        
        self.KPI = {}
        
        col = ["R2_Pow","MAPE_Pow","RMSE_Pow",
               "MAPE_COP","RMSE_COP",
               "SCOP_model","SCOP_exp","Err_SCOP [%]"]
        
        states = ["STATIONARY","MODULATION","MOD + DEF","ALL"]
        multindex = [["TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}"],states]
        multindex = pd.MultiIndex.from_product(multindex, names = ["model","status"])
        self.KPI = pd.DataFrame(self.KPI,index = multindex,columns = col)
                    
        #Filter on different stauts
        for i in range(4):
            if i == 0:
                self.HP1.test_fil = self.HP1.test[self.HP1.test['Status'] == 'STATIONARY']
                self.HP2.test_fil = self.HP2.test[self.HP2.test['Status'] == 'STATIONARY']    
            elif i == 1:
                self.HP1.test_fil = self.HP1.test[(self.HP1.test['Status'] == 'ACCELERATION') | (self.HP1.test['Status'] == 'DECELERATION')
                          | (self.HP1.test['Status'] == 'STATIONARY') | (self.HP1.test['Status'] == 'START') | (self.HP1.test['Status'] == 'STOP')]
                
                self.HP2.test_fil = self.HP2.test[(self.HP2.test['Status'] == 'ACCELERATION') | (self.HP2.test['Status'] == 'DECELERATION')
                          | (self.HP2.test['Status'] == 'STATIONARY') | (self.HP2.test['Status'] == 'START') | (self.HP2.test['Status'] == 'STOP')]
            elif i == 2:
                self.HP1.test_fil = self.HP1.test[(self.HP1.test['Status'] == 'ACCELERATION') | (self.HP1.test['Status'] == 'DECELERATION') | (self.HP1.test['Status'] == 'START')
                         | (self.HP1.test['Status'] == 'STOP') | (self.HP1.test['Status'] == 'STATIONARY') | (self.HP1.test['Status'] == 'DEF')]
                
                self.HP2.test_fil = self.HP2.test[(self.HP2.test['Status'] == 'ACCELERATION') | (self.HP2.test['Status'] == 'DECELERATION') | (self.HP2.test['Status'] == 'START')
                         | (self.HP2.test['Status'] == 'STOP') | (self.HP2.test['Status'] == 'STATIONARY') | (self.HP2.test['Status'] == 'DEF')]
            elif i == 3:
                self.HP1.test_fil = self.HP1.test[(self.HP1.test['Status'] == 'ACCELERATION') | (self.HP1.test['Status'] == 'DECELERATION')| (self.HP1.test['Status'] == 'START') | (self.HP1.test['Status'] == 'STOP')
                          | (self.HP1.test['Status'] == 'STATIONARY') | (self.HP1.test['Status'] == 'DEF')  | (self.HP1.test['Status'] == 'DHW')]
            
                self.HP2.test_fil = self.HP2.test[(self.HP2.test['Status'] == 'ACCELERATION') | (self.HP2.test['Status'] == 'DECELERATION')| (self.HP2.test['Status'] == 'START') | (self.HP2.test['Status'] == 'STOP')
                          | (self.HP2.test['Status'] == 'STATIONARY') | (self.HP2.test['Status'] == 'DEF')  | (self.HP2.test['Status'] == 'DHW')]
            
          
            #Calculate the thermodynamics variables - Train
            Delta1 = self.HP1.test_fil["LExT [°C]"]-self.HP1.test_fil["SET [°C]"]
            PLR =  self.HP1.test_fil["PLR"]
            
            #Calculate the thermodynamic variables - Test
            Delta1_exp = self.HP2.test_fil["LExT [°C]"]-self.HP2.test_fil["SET [°C]"]
            PLR_exp =  self.HP2.test_fil["PLR"]
        
            # Model input 
            X_train = np.column_stack((PLR,PLR/Delta1))
            X_test = np.column_stack((PLR_exp,PLR_exp/Delta1_exp))
            Y_train = self.HP1.test_fil["Pow [kW]"]/self.HP1.test_fil["Pow full [kW]"]
            
            #Model fitting and testing
            self.model_reg_P = linear_model.LinearRegression(fit_intercept = True).fit(X_train, Y_train)
            Pow_pred = self.model_reg_P.predict(X_test)* self.HP2.test_fil["Pow full [kW]"]
            
            #COP calculation
            COP_pred = self.HP2.test_fil["Heat Cap COND [kW]"]/Pow_pred
            COP_pred.replace([np.inf, -np.inf], np.nan, inplace=True)
            COP_pred.fillna(0, inplace = True)
            
            #SCOP calculation
            SCOP_model = sum(np.array(self.HP2.test_fil["Heat Cap COND [kW]"]))/sum(Pow_pred)
            SCOP_exp = sum(np.array(self.HP2.test_fil["Heat Cap COND [kW]"]))/sum(np.array(self.HP2.test_fil["Pow [kW]"]))
        
            #KPI Calculations 
            if i == 0:
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","STATIONARY"),"R2_Pow"] = float(r2_score(self.HP2.test_fil["Pow [kW]"],Pow_pred))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","STATIONARY"),"MAPE_Pow"] = float(mean_absolute_percentage_error(self.HP2.test_fil["Pow [kW]"],Pow_pred))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","STATIONARY"),"RMSE_Pow"] = float(root_mean_squared_error(self.HP2.test_fil["Pow [kW]"],Pow_pred).astype(float))
                
                # #COP
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","STATIONARY"),"MAPE_COP"] = float(mean_absolute_percentage_error(self.HP2.test_fil["COP"],COP_pred))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","STATIONARY"),"RMSE_COP"] = float(root_mean_squared_error(self.HP2.test_fil["COP"],COP_pred).astype(float))
                  
                #SCOP
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","STATIONARY"),"SCOP_model"] = float(SCOP_model.astype(float))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","STATIONARY"),"SCOP_exp"] = float(SCOP_exp.astype(float))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","STATIONARY"),"Err_SCOP [%]"] = float((SCOP_model - SCOP_exp)/SCOP_exp *100)
                
               #Plot
               # self.HP2.plot_power_model(Pow_pred,"STATIONARY")
               # self.HP2.plot_COP_model(COP_pred,"STATIONARY")
               # self.HP2.Err_Power(Pow_pred, "STATIONARY")
               
        
            elif i == 1:
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","MODULATION"),"R2_Pow"] = float(r2_score(self.HP2.test_fil["Pow [kW]"],Pow_pred))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","MODULATION"),"MAPE_Pow"] = float(mean_absolute_percentage_error(self.HP2.test_fil["Pow [kW]"],Pow_pred))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","MODULATION"),"RMSE_Pow"] = float(root_mean_squared_error(self.HP2.test_fil["Pow [kW]"],Pow_pred).astype(float))
                
                #COP
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","MODULATION"),"MAPE_COP"] = float(mean_absolute_percentage_error(self.HP2.test_fil["COP"],COP_pred))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","MODULATION"),"RMSE_COP"] = float(root_mean_squared_error(self.HP2.test_fil["COP"],COP_pred).astype(float))
                
                #SCOP
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","MODULATION"),"SCOP_model"] = float(SCOP_model.astype(float))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","MODULATION"),"SCOP_exp"] = float(SCOP_exp.astype(float))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","MODULATION"),"Err_SCOP [%]"] = float((SCOP_model - SCOP_exp)/SCOP_exp *100)
                
               #Plot
               # self.HP2.plot_power_model(Pow_pred,"MODULATION")
               # self.HP2.plot_COP_model(COP_pred,"MODULATION")
               # self.HP2.Err_Power(Pow_pred, "MODULATION")
             
               
            elif i == 2:
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","MOD + DEF"),"R2_Pow"] = float(r2_score(self.HP2.test_fil["Pow [kW]"],Pow_pred))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","MOD + DEF"),"MAPE_Pow"] = float(mean_absolute_percentage_error(self.HP2.test_fil["Pow [kW]"],Pow_pred))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","MOD + DEF"),"RMSE_Pow"] = float(root_mean_squared_error(self.HP2.test_fil["Pow [kW]"],Pow_pred).astype(float))
                
                #COP
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","MOD + DEF"),"MAPE_COP"] = float(mean_absolute_percentage_error(self.HP2.test_fil["COP"],COP_pred))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","MOD + DEF"),"RMSE_COP"] = float(root_mean_squared_error(self.HP2.test_fil["COP"],COP_pred).astype(float))
                
                #SCOP
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","MOD + DEF"),"SCOP_model"] = float(SCOP_model.astype(float))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","MOD + DEF"),"SCOP_exp"] = float(SCOP_exp.astype(float))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","MOD + DEF"),"Err_SCOP [%]"] = float((SCOP_model - SCOP_exp)/SCOP_exp *100)
                
               #Plot
               # self.HP2.plot_power_model(Pow_pred,"MOD + DEF")
               # self.HP2.plot_COP_model(COP_pred,"MOD + DEF")
               # self.HP2.Err_Power(Pow_pred, "MOD + DEF")
              
                
            elif i == 3:
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","ALL"),"R2_Pow"] = float(r2_score(self.HP2.test_fil["Pow [kW]"],Pow_pred))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","ALL"),"MAPE_Pow"] = float(mean_absolute_percentage_error(self.HP2.test_fil["Pow [kW]"],Pow_pred))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","ALL"),"RMSE_Pow"] = float(root_mean_squared_error(self.HP2.test_fil["Pow [kW]"],Pow_pred).astype(float))
                
                #COP
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","ALL"),"MAPE_COP"] = float(mean_absolute_percentage_error(self.HP2.test_fil["COP"],COP_pred))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","ALL"),"RMSE_COP"] = float(root_mean_squared_error(self.HP2.test_fil["COP"],COP_pred).astype(float))
                
                #SCOP
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","ALL"),"SCOP_model"] = float(SCOP_model.astype(float))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","ALL"),"SCOP_exp"] = float(SCOP_exp.astype(float))
               self.KPI.loc[("TRAIN:" + f" {self.HP1.name}"+"\nTEST: "+ f" {self.HP2.name}","ALL"),"Err_SCOP [%]"] = float((SCOP_model - SCOP_exp)/SCOP_exp *100)
                
               #Plot
               # self.HP2.plot_power_model(Pow_pred,"ALL")
               # self.HP2.plot_COP_model(COP_pred,"ALL")
               # self.HP2.Err_Power(Pow_pred, "ALL")
             
              
        return self.KPI





















