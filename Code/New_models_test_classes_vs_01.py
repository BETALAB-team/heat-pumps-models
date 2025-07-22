from New_models_classes_vs_01 import *
from matplotlib.ticker import FormatStrFormatter
#%%Methods

#Barplot
def barplot(KPI):

    #Create figures
    figure1, axs1 = plt.subplots(3,1,figsize = (19,9.5))
    sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
    
    
    #Create labels
    model = ["VA+ ID5", "VA+ ID9","VA+ ID24","R_NXHM ID458","R_NXHM ID526","N 2050 ID167","N 2050 ID531","N F2040 ID61" ,"MT AQ30I ID598"]
    
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
    br3 = [x + barWidth for x in br2] 
    
    
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
    plt.savefig(os.path.join('..',"Result Analysis","New models results","New_Models_KPI_weight_no_DeltaT^2.png"))
    plt.close()
    
    #Create figures
    # figure2, axs2 = plt.subplots(2,1,figsize = (19,9.5))
    # sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
    
    # #Create barplot 2
    # axs2[0].bar(br1, np.array(SCOP_mod_stat), width = barWidth, label = "Model")
    # axs2[0].bar(br2, np.array(SCOP_exp_stat), width = barWidth, label = 'Experimental')
    # axs2[0].set_xticks(br3,model)
    # axs2[0].tick_params(axis='y')
    # axs2[0].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    # axs2[0].set_ylabel("SCOP_stat")
    
    # axs2[1].bar(br1, np.array(SCOP_mod_all), width = barWidth, label = "Model")
    # axs2[1].bar(br2, np.array(SCOP_exp_all), width = barWidth, label = 'Experimental')
    # axs2[1].set_xticks(br3,model)
    # axs2[1].tick_params(axis='y')
    # axs2[1].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    # axs2[1].set_ylabel("SCOP_all")
    # axs2[1].legend()
    
    figure2, axs2 = plt.subplots(1,figsize = (19,9.5))
    sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
    
    #Create barplot 2
    axs2.bar(br1, np.array(SCOP_mod_all), width = barWidth, label = "Model", color = "blue")
    axs2.bar(br2, np.array(SCOP_exp_stat), width = barWidth, label = 'Experimental - STAT', color = "orange", hatch='///')
    axs2.bar(br3, np.array(SCOP_exp_all), width = barWidth, label = 'Experimental - ALL',color = "orange")
    axs2.set_xticks(br2,model)
    
    axs2.tick_params(axis='y')
    axs2.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    # axs2.set_ylabel("SCOP")
    axs2.legend()    
    
    figure2.suptitle("SCOP")
    plt.tight_layout()
    plt.savefig(os.path.join('..',"Result Analysis","New models results","SCOP_weight_no_DeltaT^2.png"))
    plt.close()

def barplot_ML(KPI):

    #Create figures
    figure1, axs1 = plt.subplots(3,1,figsize = (19,9.5))
    sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
    
    
    #Create labels
    model = ["VA+ ID5", "VA+ ID9","VA+ ID24","R_NXHM ID458","R_NXHM ID526","N 2050 ID167","N 2050 ID531","N F2040 ID61" ,"MT AQ30I ID598"]
    
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
    br3 = [x + barWidth for x in br2] 
    
    
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
    
    figure1.suptitle("KPIs_ML")
    plt.tight_layout()
    plt.savefig(os.path.join('..',"Result Analysis","New models results","New_Models_KPI_ML.png"))
    plt.close()
    
    figure2, axs2 = plt.subplots(1,figsize = (19,9.5))
    sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
    
    #Create barplot 2
    axs2.bar(br1, np.array(SCOP_mod_all), width = barWidth, label = "Model", color = "blue")
    axs2.bar(br2, np.array(SCOP_exp_stat), width = barWidth, label = 'Experimental - STAT', color = "orange", hatch='///')
    axs2.bar(br3, np.array(SCOP_exp_all), width = barWidth, label = 'Experimental - ALL',color = "orange")
    axs2.set_xticks(br2,model)
    
    axs2.tick_params(axis='y')
    axs2.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs2.legend()    
    
    figure2.suptitle("SCOP_ML")
    plt.tight_layout()
    plt.savefig(os.path.join('..',"Result Analysis","New models results","SCOP_ML.png"))
    plt.close()
    
#%% Devices lists

devices = [
           ("Valliant A+ 5kW  ID5 01-11-2022_28-02-2023", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           ("Valliant A+ 5kW  ID9 01-11-2022_28-02-2023", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           ("Valliant A+ 5kW  ID24 01-11-2022_28-02-2023", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           
           ("Riello NXHM 10 kW ID458 01-11-2024_28-02-2025","Riello NXHM 10 kW - DATA","AtW"),
           ("Riello NXHM 10 kW ID526 01-11-2024_28-02-2025","Riello NXHM 10 kW - DATA","AtW"),
           
           ("NIBE 2050 10 kW ID167 01-11-2024_28-02-2025","NIBE 2050 10 kW - DATA","AtW"),
           ("NIBE 2050 10 kW ID531 01-11-2024_28-02-2025","NIBE 2050 10 kW - DATA","AtW"),
           
           ("NIBE F2040 12 kW ID61 01-11-2024_28-02-2025","NIBE F2040 12 kW - DATA","AtW"),
           
           ("MT AQ30I 8 kW ID598 01-11-2024_28-02-2025","MT AQ30I 8  kW - DATA","WtW")
           ]

#For loop
KPIs = []
KPIs_ML = []

for dev in devices:
    
    HP = Heat_Pumps(dev)
    HP.status_analysis()
    HP.interp_full_load()
    HP.new_model_fit()
    HP.new_model_fit_ML()
    KPIs.append(HP.KPI)
    KPIs_ML.append(HP.KPI_ML)
    # HP.plot_test("2025-02-15 00:00:00","2025-02-20 00:00:00" )
    # HP.plot_full_load()
    
KPIs = pd.concat(KPIs)
KPIs_ML = pd.concat(KPIs_ML)

barplot(KPIs)
barplot_ML(KPIs_ML)

        
        
        
        
