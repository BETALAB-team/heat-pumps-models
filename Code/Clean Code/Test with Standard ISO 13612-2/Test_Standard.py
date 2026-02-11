import numpy as np
from New_models_classes_vs_01 import *
from matplotlib.ticker import FormatStrFormatter
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error,r2_score,mean_absolute_error
import matplotlib.pyplot as plt

#%% Set Seaborn theme and set working directory

sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
os.chdir('..')

#%% Class for standard calculation 

devices = [ 
           # ("Valliant A+ 5kW ID9 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           # ("Riello NXHM 10 kW ID526 01-09-2024_30-04-2025","Riello NXHM 10 kW - DATA","AtW"),
           # ("NIBE 2050 10 kW ID167 01-09-2024_30-04-2025","NIBE 2050 10 kW - DATA","AtW"),
           # ("NIBE F2040 12 kW ID61 01-09-2024_30-04-2025","NIBE F2040 12 kW - DATA","AtW"),
           ("Valliant A+ 12kW ID196 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW")
          
           ]
def relative_mean_absolute_error(y_true, y_pred):
    return 1/np.mean(y_true) * np.mean(np.abs(y_true - y_pred)) * 100 

def CV_RMSE(y_true,y_pred):
    return 1/np.mean(y_true)*root_mean_squared_error(y_true,y_pred)*100

for dev in devices:
    
    HP = Heat_Pumps(dev) 
    HP.status_analysis()
    HP.interp_full_load()
    HP.new_model_fit()
    HP.test_fil["COP full"] = HP.test_fil["Heat Cap COND full [kW]"] / HP.test_fil["Pow full [kW]"]
    
    #Use SetData_s for Valliant, otherwise SetData for other HPs
    df_std = pd.read_excel(os.path.join('..','Data', f"{HP.catalogue_data}.xlsx"), sheet_name = "SetData_s")
    # df_std = pd.read_excel(os.path.join('..','Data', f"{HP.catalogue_data}.xlsx"), sheet_name = "SetData")
    df_std_part = df_std.loc[(df_std["LExT [°C]"] == 55) & (df_std["PLR"] < 1)]
    df_std_full = df_std.loc[(df_std["LExT [°C]"] == 55) & (df_std["PLR"] == 1)]
    # df_std_full = df_std.loc[(df_std["LExT [°C]"] == 35) & (df_std["PLR"] == 1) & (df_std["SET [°C]"] >= 2) & (df_std["SET [°C]"] <= 12)]
    
    
    #Create database for training
    Train = pd.DataFrame(columns = ["PLR","f_cop"])
    Train["f_cop"] = np.concatenate([[0],[1],df_std_part["COP"].to_numpy()/ df_std_full["COP"].to_numpy()])
    Train["PLR"] = np.concatenate([[0],[1],df_std_part["PLR"].to_numpy()])
    Train.sort_values("PLR", inplace= True)
    df = HP.test_fil.loc[(HP.test_fil["PLR"] != 0) & (HP.test_fil["PLR"] <= 1) ]
    # df = df.loc[df["Status"] == "STEADY STATE"]
    
    #Picewise linear regression model Standard ISO 13612-2
    f_cop = np.interp(df["PLR"], Train["PLR"], Train["f_cop"])
  
    
    #Error calculation
    COP_mod = f_cop * df["COP full"]
    Pow_std = df["Heat Cap COND [kW]"]/COP_mod
    Err = (COP_mod -df["COP"])/df["COP"] * 100
    Err_Pow_mod = (df["Pow_pred"] - df["Pow [kW]"])/np.mean(df["Pow [kW]"])*100
    Err_Pow_std = (Pow_std - df["Pow [kW]"])/np.mean(df["Pow [kW]"])*100
    
    #KPI calculation
    r2_Pow_std = r2_score(df["Pow [kW]"],Pow_std)
    r2_Pow_mod = r2_score(df["Pow [kW]"],df["Pow_pred"])
    mae_Pow_std =  relative_mean_absolute_error(df["Pow [kW]"],Pow_std)
    mae_Pow_mod =  relative_mean_absolute_error(df["Pow [kW]"],df["Pow_pred"])
    cvrmse_Pow_std =  CV_RMSE(df["Pow [kW]"],Pow_std)
    cvrmse_Pow_mod =  CV_RMSE(df["Pow [kW]"],df["Pow_pred"])
    
    print ("R2_std = ",r2_Pow_std )
    print ("rMAE_std = ", mae_Pow_std )
    print ("cvrmse std = ", cvrmse_Pow_std)
    print("R2_mod = ",r2_Pow_mod)
    print ("rMAE_mod = ", mae_Pow_mod)
    print ("cvrmse mod = ", cvrmse_Pow_mod)
    

#%% Plot

# figure1, axs1= plt.subplots(1,2,figsize = (19,9.5))
# axs1[0].scatter(df["PLR"], Err_Pow_std , c = "#13315c", label = "Power_model")
# axs1[0].set_xlabel("PLR", fontsize = 20)
# # axs1[0].set_xlim(0.2,1)
# # axs1[0].set_ylim(-100,100)
# axs1[0].set_ylabel("Err [%]", fontsize = 20)
# axs1[0].tick_params(axis='x',labelsize = 20)
# axs1[0].tick_params(axis='y',labelsize = 20)


# axs1[1].scatter(df["PLR"], Err_Pow_mod,c = '#fca151', label = "Power_model")
# axs1[1].set_xlabel("PLR", fontsize = 20)
# # axs1[1].set_xlim(0.2,1)
# # axs1[1].set_ylim(-100,100)
# axs1[1].set_ylabel("Err_Pow [%]", fontsize = 20)
# axs1[1].tick_params(axis='x',labelsize = 20)
# axs1[1].tick_params(axis='y',labelsize = 20)

# figure2, axs2= plt.subplots(1,figsize = (19,9.5))
# axs2.scatter(df["PLR"], Err_Pow_mod/Err_Pow_std , c = "#13315c", label = "Power_model")
# axs2.set_xlabel("PLR", fontsize = 20)
# # axs1[0].set_xlim(0.2,1)
# axs2.set_ylim(-100,100)
# axs2.set_ylabel("Err [%]", fontsize = 20)
# axs2.tick_params(axis='x',labelsize = 20)
# axs2.tick_params(axis='y',labelsize = 20)
