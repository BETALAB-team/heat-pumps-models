import os 
import pandas as pd
import numpy as np
import pwlf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import linear_model
from scipy.optimize import curve_fit
from sklearn.metrics import mean_absolute_error, root_mean_squared_error,r2_score,mean_absolute_percentage_error
from New_models_preprocess_vs_02 import *
from matplotlib.ticker import FormatStrFormatter
import statsmodels.api as sm

#%%
#Barplot
def barplot(KPI):

    #Create figures
    figure1, axs1 = plt.subplots(3,1,figsize = (19,9.5))
    sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
    
    
    #Create labels
    model = ["VA+ ID5", "VA+ ID9","VA+ ID24","R_NXHM ID458","R_NXHM ID526","N 2050 ID167","N 2050 ID531","N F2040 ID61" ]
    
    R2_stat = KPI.loc[KPI.index.get_level_values("status") == "STATIONARY","R2_Pow"]
    R2_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","R2_Pow"]  
    
    MAPE_stat = KPI.loc[KPI.index.get_level_values("status") == "STATIONARY","MAPE_Pow"]
    MAPE_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","MAPE_Pow"]  
    
    RMSE_stat = KPI.loc[KPI.index.get_level_values("status") == "STATIONARY","RMSE_Pow"]
    RMSE_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","RMSE_Pow"]  
    
    Err_SCOP_stat = KPI.loc[KPI.index.get_level_values("status") == "STATIONARY","Err_SCOP"]
    Err_SCOP_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","Err_SCOP"]  
    
    SCOP_mod_stat = KPI.loc[KPI.index.get_level_values("status") == "STATIONARY","SCOP_model"]
    SCOP_exp_stat = KPI.loc[KPI.index.get_level_values("status") == "STATIONARY","SCOP_exp"]
    
    SCOP_mod_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","SCOP_model"]  
    SCOP_exp_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","SCOP_exp"]  
    
    
    #Create bar
    barWidth = 0.2
    br1 = np.arange(len(R2_all)) 
    br2 = [x + barWidth for x in br1] 
    br3 = [x + barWidth/2 for x in br1] 
    
    
    #Create barplot 1 
    axs1[0].bar(br1, np.array(R2_stat), width = barWidth, label = "STATIONARY")
    axs1[0].bar(br2, np.array(R2_all), width = barWidth, label = 'ALL')
    axs1[0].set_xticks(br3,model)
    axs1[0].tick_params(axis='y')
    axs1[0].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs1[0].set_ylabel("R2")
    axs1[0].set_ylim(0,1)
    
    axs1[1].bar(br1, np.array(MAPE_stat), width = barWidth, label = "STATIONARY")
    axs1[1].bar(br2, np.array(MAPE_all), width = barWidth, label = 'ALL')
    axs1[1].set_xticks(br3,model)
    axs1[1].tick_params(axis='y')
    axs1[1].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs1[1].set_ylabel("MAPE")
    axs1[1].set_ylim(0,1)
    axs1[1].legend()
    
    axs1[2].bar(br1, np.array(RMSE_stat), width = barWidth, label = "STATIONARY")
    axs1[2].bar(br2, np.array(RMSE_all), width = barWidth, label = 'ALL')
    axs1[2].set_xticks(br3,model)
    axs1[2].tick_params(axis='y')
    axs1[2].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs1[2].set_ylabel("RMSE")
    axs1[2].set_ylim(0,1)
    
    figure1.suptitle("KPIs")
    plt.tight_layout()
    plt.savefig(os.path.join('..',"Result Analysis","New_Models_KPI_weight_no_DeltaT^2.png"))
    plt.close()
    
    #Create figures
    figure2, axs2 = plt.subplots(2,1,figsize = (19,9.5))
    sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
    
    #Create barplot 2
    axs2[0].bar(br1, np.array(SCOP_mod_stat), width = barWidth, label = "Model")
    axs2[0].bar(br2, np.array(SCOP_exp_stat), width = barWidth, label = 'Experimental')
    axs2[0].set_xticks(br3,model)
    axs2[0].tick_params(axis='y')
    axs2[0].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs2[0].set_ylabel("SCOP_stat")
    
    axs2[1].bar(br1, np.array(SCOP_mod_all), width = barWidth, label = "Model")
    axs2[1].bar(br2, np.array(SCOP_exp_all), width = barWidth, label = 'Experimental')
    axs2[1].set_xticks(br3,model)
    axs2[1].tick_params(axis='y')
    axs2[1].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs2[1].set_ylabel("SCOP_all")
    axs2[1].legend()
    
    
    figure2.suptitle("SCOP_filt_catalogue")
    plt.tight_layout()
    plt.savefig(os.path.join('..',"Result Analysis","SCOP_weight_no_DeltaT^2.png"))
    plt.close()

def plot_COP_model(exp,dev, COP_pred,status):
    
    #Create folder
    if not os.path.exists(os.path.join('..',"Results",dev)):
        os.mkdir(os.path.join('..',"Results",dev))
    else:
        pass
    
    if not os.path.exists(os.path.join('..',"Results",f"{dev}","New_models")):
        os.mkdir(os.path.join('..',"Results",dev,"New_models"))
    else:
        pass


    #Plot Power_pred vs Power_real 
    figure3, axs3 = plt.subplots(1, figsize = (19,9.5))
    sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')

    plt.scatter(np.array(exp["COP"]),COP_pred, c = exp["PLR"], cmap='jet', label = "COP_model")
    plt.plot([0, 10], [0, 10], "k--", label = "Bisector")
    plt.plot([0, 10], [0, 12], "k--", label = "Error +20%")                    
    plt.text( 6, 4.5, "-20%")
    plt.plot([0, 10], [0, 8], "k--", label = "Error -20%")
    plt.text( 6, 7.7, "+20%")
    cbar = plt.colorbar()
    cbar.set_label("PLR")
    plt.xlabel("COP_exp [kW]")
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.ylabel('COP_model[kW]')
    plt.legend()
    
    # plt.tight_layout()
    plt.savefig(os.path.join('..',"Results",f"{dev}","New_models",f"NEW_MODEL_COP_{status}.png"))
    plt.close()

    
#Define new model
def new_model(devices, tupler):        
    KPI = {}
    col = ["R2_Pow","MAPE_Pow","RMSE_Pow",
           "MAPE_COP","RMSE_COP",
           "SCOP_model","SCOP_exp","Err_SCOP"]
    
    states = ["STATIONARY","MODULATION","MOD + DEF","ALL"]
    multindex = [devices,states]
    multindex = pd.MultiIndex.from_product(multindex, names = ["model","status"])
    KPI = pd.DataFrame(KPI,index = multindex,columns = col)
    
    #Clear the data
    for dev,cat in tupler:
        
        #Import entire database for the specific device
        data = pd.read_excel(os.path.join('..','Data',f"{dev}.xlsx"), sheet_name = "Test")
        data = data.loc[:, ~data.columns.str.contains('^Unnamed')] 
        
        #Test with just PLR >= 0.25 to veirfy if it is necessary to split the equation in two
        # data = data.loc[data["PLR"] >= 0.25]
    
        #Import the catalogue data  with the PLR calculation
        catalogue_data =  pd.read_excel(os.path.join('..','Data',f"{cat}.xlsx"),sheet_name="SetData")    
        
        #Filter
        for i in range(4):
            if i == 0:
               exp = data[data['Status'] == 'STATIONARY']
            elif i == 1:
                exp = data[(data['Status'] == 'ACCELERATION') | (data['Status'] == 'DECELERATION')
                          | (data['Status'] == 'STATIONARY') | (data['Status'] == 'START') | (data['Status'] == 'STOP')]
            elif i == 2:
                exp = data[(data['Status'] == 'ACCELERATION') | (data['Status'] == 'DECELERATION')
                          | (data['Status'] == 'STATIONARY') | (data['Status'] == 'DEF')| (data['Status'] == 'START') | (data['Status'] == 'STOP')]
            elif i == 3:
                exp = data[(data['Status'] == 'ACCELERATION') | (data['Status'] == 'DECELERATION')
                          | (data['Status'] == 'STATIONARY') | (data['Status'] == 'DEF')  | (data['Status'] == 'DHW')| (data['Status'] == 'START') | (data['Status'] == 'STOP')]
                    
            #Normalize the thermodynamics variables - Catalogues
            # Pow_fl = catalogue_data.loc[(catalogue_data["SET [°C]"] == -7) & (catalogue_data["LExT [°C]"] == 35) &
                                        # (catalogue_data["PLR"] == 1),"Pow [kW]"].item()
            
            # SET = (catalogue_data["SET [°C]"] + 273.15)/(-7 + 273.15)
            # LExT =  (catalogue_data["LExT [°C]"] + 273.15)/(35 + 273.15)
            # Delta1 = (catalogue_data["LExT [°C]"]-catalogue_data["SET [°C]"])/(35 + 7)
            Delta1 = (catalogue_data["LExT [°C]"]-catalogue_data["SET [°C]"])
            PLR =  catalogue_data["PLR"]
        
             # #Normalize the thermodinamics variables - Experimental Data 
            # SET_exp = (exp["SET [°C]"] + 273.15)/(-7 + 273.15)
            # LExT_exp =  (exp["LExT [°C]"] + 273.15)/(35 + 273.15)
            # Delta1_exp = (exp["LExT [°C]"]-exp["SET [°C]"])/(35 + 7 )
            Delta1_exp = (exp["LExT [°C]"]-exp["SET [°C]"])
            PLR_exp =  exp["PLR"]
                    
            
             # Model input - alternative equation
            X_train = np.column_stack((PLR,PLR/Delta1))
            X_test = np.column_stack((PLR_exp,PLR_exp/Delta1_exp))
            Y_train = catalogue_data["Pow [kW]"]/catalogue_data["Pow full [kW]"]

            #Linear model and evaluation of reisudals
            # X_train = sm.add_constant(X_train)
            # ols_model_Pow = sm.OLS(Y_train,X_train).fit()
            # residuals_Pow = ols_model_Pow.resid
            # weights_pow = 1 /abs(residuals_Pow)  
            
            # #Second Training - Power
            # X_test = sm.add_constant(X_test)
            # model_Pow_weight = sm.WLS(Y_train, X_train, weights= weights_pow)
            # model_Pow_weight = model_Pow_weight.fit()
            
            
            model_reg_P = linear_model.LinearRegression(fit_intercept = True).fit(X_train, Y_train)
            print(model_reg_P.coef_)
            Pow_pred = model_reg_P.predict(X_test)* exp["Pow full [kW]"]
            # Pow_pred = model_Pow_weight.predict(X_test)* exp["Pow full [kW]"]
            
            # Picewise regression
            # model_reg_Pow = pwlf.PiecewiseLinFit(catalogue_data["PLR"],catalogue_data["Pow [kW]"]/catalogue_data["Pow full [kW]"])
            # z = model_reg_Pow.fit_with_breaks([0,0.25,1])
            # Pow_ratio_pred = model_reg_Pow.predict(exp["PLR"])
            # Pow_pred = Pow_ratio_pred* exp["Pow full [kW]"]
             # Model input - alternative equation
             


            #COP calculation
            COP_pred = exp["Heat Cap COND [kW]"]/Pow_pred
            COP_pred.replace([np.inf, -np.inf], np.nan, inplace=True)
            COP_pred.fillna(0, inplace = True)
            COP_fl_model = exp["Heat Cap COND full [kW]"]/ exp["Pow full [kW]"]
            
            
            
            #SCOP calculation
            SCOP_model = sum(np.array(exp["Heat Cap COND [kW]"]))/sum(Pow_pred)
            SCOP_exp = sum(np.array(exp["Heat Cap COND [kW]"]))/sum(np.array(exp["Pow [kW]"]))
        
            #KPI Calculations 
            if i == 0:
                KPI.loc[(dev,"STATIONARY"),"R2_Pow"] = float(r2_score(exp["Pow [kW]"],Pow_pred))
                KPI.loc[(dev,"STATIONARY"),"MAPE_Pow"] = float(mean_absolute_error(exp["Pow [kW]"],Pow_pred))
                KPI.loc[(dev,"STATIONARY"),"RMSE_Pow"] = float(root_mean_squared_error(exp["Pow [kW]"],Pow_pred).astype(float))
                
                # #COP
                KPI.loc[(dev,"STATIONARY"),"MAPE_COP"] = float(mean_absolute_error(exp["COP"],COP_pred))
                KPI.loc[(dev,"STATIONARY"),"RMSE_COP"] = float(root_mean_squared_error(exp["COP"],COP_pred).astype(float))
                  
                #SCOP
                KPI.loc[(dev,"STATIONARY"),"SCOP_model"] = float(SCOP_model.astype(float))
                KPI.loc[(dev,"STATIONARY"),"SCOP_exp"] = float(SCOP_exp.astype(float))
                KPI.loc[(dev,"STATIONARY"),"Err_SCOP"] = float(abs(SCOP_exp - SCOP_model))
                
                #Plot
                # plot_power_model(exp, dev, Pow_pred,"STATIONARY")
                # plot_COP_model(exp,dev, COP_pred,"STATIONARY")
    
            elif i == 1:
                KPI.loc[(dev,"MODULATION"),"R2_Pow"] = float(r2_score(exp["Pow [kW]"],Pow_pred))
                KPI.loc[(dev,"MODULATION"),"MAPE_Pow"] = float(mean_absolute_error(exp["Pow [kW]"],Pow_pred))
                KPI.loc[(dev,"MODULATION"),"RMSE_Pow"] = float(root_mean_squared_error(exp["Pow [kW]"],Pow_pred).astype(float))
                
                #COP
                KPI.loc[(dev,"MODULATION"),"MAPE_COP"] = float(mean_absolute_error(exp["COP"],COP_pred))
                KPI.loc[(dev,"MODULATION"),"RMSE_COP"] = float(root_mean_squared_error(exp["COP"],COP_pred).astype(float))
                
                #SCOP
                KPI.loc[(dev,"MODULATION"),"SCOP_model"] = float(SCOP_model.astype(float))
                KPI.loc[(dev,"MODULATION"),"SCOP_exp"] = float(SCOP_exp.astype(float))
                KPI.loc[(dev,"MODULATION"),"Err_SCOP"] = float(abs(SCOP_exp - SCOP_model))
                
                #Plot
                # plot_power_model(exp,dev, Pow_pred,"MODULATION")
                # plot_COP_model(exp,dev, COP_pred,"MODULATION")
            
            elif i == 2:
                KPI.loc[(dev,"MOD + DEF"),"R2_Pow"] = float(r2_score(exp["Pow [kW]"],Pow_pred))
                KPI.loc[(dev,"MOD + DEF"),"MAPE_Pow"] = float(mean_absolute_error(exp["Pow [kW]"],Pow_pred))
                KPI.loc[(dev,"MOD + DEF"),"RMSE_Pow"] = float(root_mean_squared_error(exp["Pow [kW]"],Pow_pred).astype(float))
                
                #COP
                KPI.loc[(dev,"MOD + DEF"),"MAPE_COP"] = float(mean_absolute_error(exp["COP"],COP_pred))
                KPI.loc[(dev,"MOD + DEF"),"RMSE_COP"] = float(root_mean_squared_error(exp["COP"],COP_pred).astype(float))
                
                #SCOP
                KPI.loc[(dev,"MOD + DEF"),"SCOP_model"] = float(SCOP_model.astype(float))
                KPI.loc[(dev,"MOD + DEF"),"SCOP_exp"] = float(SCOP_exp.astype(float))
                KPI.loc[(dev,"MOD + DEF"),"Err_SCOP"] = float(abs(SCOP_exp - SCOP_model))
                
                #Plot
                # plot_power_model(exp,dev, Pow_pred,"MOD + DEF")
                # plot_COP_model(exp,dev, COP_pred,"MOD + DEF")
                
            elif i == 3:
                KPI.loc[(dev,"ALL"),"R2_Pow"] = float(r2_score(exp["Pow [kW]"],Pow_pred))
                KPI.loc[(dev,"ALL"),"MAPE_Pow"] = float(mean_absolute_error(exp["Pow [kW]"],Pow_pred))
                KPI.loc[(dev,"ALL"),"RMSE_Pow"] = float(root_mean_squared_error(exp["Pow [kW]"],Pow_pred).astype(float))
                
                #COP
                KPI.loc[(dev,"ALL"),"MAPE_COP"] = float(mean_absolute_error(exp["COP"],COP_pred))
                KPI.loc[(dev,"ALL"),"RMSE_COP"] = float(root_mean_squared_error(exp["COP"],COP_pred).astype(float))
                
                #SCOP
                KPI.loc[(dev,"ALL"),"SCOP_model"] = float(SCOP_model.astype(float))
                KPI.loc[(dev,"ALL"),"SCOP_exp"] = float(SCOP_exp.astype(float))
                KPI.loc[(dev,"ALL"),"Err_SCOP"] = float(abs(SCOP_exp - SCOP_model))
                
                #Plot
                # plot_power_model(exp,dev, Pow_pred,"ALL")
                # plot_COP_model(exp,dev, COP_pred,"ALL")
                
    return KPI, Pow_pred

#%% Test the models

devices = [
       "Valliant A+ 5kW  ID5 01-11-2022_28-02-2023",
       "Valliant A+ 5kW  ID9 01-11-2022_28-02-2023",
       "Valliant A+ 5kW  ID24 01-11-2022_28-02-2023",
       
       "Riello NXHM 10 kW ID458 01-11-2024_28-02-2025",
       "Riello NXHM 10 kW ID526 01-11-2024_28-02-2025",
       
       "NIBE 2050 10 kW ID167 01-11-2024_28-02-2025",
       "NIBE 2050 10 kW ID531 01-11-2024_28-02-2025",
       
       "NIBE F2040 12 kW ID61 01-11-2024_28-02-2025",
     
       ]
       
tupler = [ 
       # ("Riello NXHM 10 kW ID458 01-11-2024_28-02-2025","Riello NXHM 10 kW - DATA"),
       # ("Riello NXHM 10 kW ID526 01-11-2024_28-02-2025","Riello NXHM 10 kW - DATA"),
       
       ("NIBE 2050 10 kW ID167 01-11-2024_28-02-2025","NIBE 2050 10 kW - DATA"),
       ("NIBE 2050 10 kW ID531 01-11-2024_28-02-2025","NIBE 2050 10 kW - DATA"),
       
       # ("NIBE F2040 12 kW ID61 01-11-2024_28-02-2025","NIBE F2040 12 kW - DATA"),
       
       ]

KPI, Pow_pred = new_model(devices,tupler)
# barplot(KPI)












