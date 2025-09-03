from New_models_classes_vs_01 import *
from matplotlib.ticker import FormatStrFormatter
#%% Set Seaborn theme
sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')

#%%Plots
def barplot(model,KPI,font):

    #Create figures
    figure1, axs1 = plt.subplots(3,1,figsize = (19,9.5))
       
    #Create labels

    
    R2_stat = KPI.loc[KPI.index.get_level_values("status") == "STATIONARY","R2_Pow"]
    R2_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","R2_Pow"]  
    
    MAPE_stat = KPI.loc[KPI.index.get_level_values("status") == "STATIONARY","MAPE_Pow"]
    MAPE_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","MAPE_Pow"]  
    
    RMSE_stat = KPI.loc[KPI.index.get_level_values("status") == "STATIONARY","RMSE_Pow"]
    RMSE_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","RMSE_Pow"]  
    
    Err_SCOP_stat = KPI.loc[KPI.index.get_level_values("status") == "STATIONARY","Err_SCOP [%]"]
    Err_SCOP_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","Err_SCOP [%]"]  
    
    SCOP_mod_stat = KPI.loc[KPI.index.get_level_values("status") == "STATIONARY","SCOP_model"]
    SCOP_exp_stat = KPI.loc[KPI.index.get_level_values("status") == "STATIONARY","SCOP_exp"]
    
    SCOP_mod_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","SCOP_model"]  
    SCOP_exp_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","SCOP_exp"]  
    
    
    #Create bar
    barWidth = 0.2
    br1 = np.arange(len(R2_all)) 
    brn = [x + barWidth/2 for x in br1] 
    br2 = [x + barWidth for x in br1] 
    br3 = [x + barWidth for x in br2] 
    
    
    #Create barplot 1 
    axs1[0].bar(br1, np.array(R2_stat), width = barWidth, label = "STATIONARY")
    axs1[0].bar(br2, np.array(R2_all), width = barWidth, label = 'ALL')
    axs1[0].set_xticks(brn)
    axs1[0].set_xticklabels(model,rotation = 45,fontsize = font)
    axs1[0].tick_params(axis='y', labelsize = font)
    axs1[0].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs1[0].set_ylabel("R2", fontsize = font)
    axs1[0].set_ylim(0,1)
    
    axs1[1].bar(br1, np.array(MAPE_stat), width = barWidth, label = "STATIONARY")
    axs1[1].bar(br2, np.array(MAPE_all), width = barWidth, label = 'ALL')
    axs1[1].set_xticks(brn)
    axs1[1].set_xticklabels(model,rotation = 45,fontsize = font)
    axs1[1].tick_params(axis='y', labelsize = font)
    axs1[1].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs1[1].set_ylabel("MAPE",fontsize = font)
    axs1[1].set_ylim(0,1)
    axs1[1].legend(fontsize = font)
    
    axs1[2].bar(br1, np.array(RMSE_stat), width = barWidth, label = "STATIONARY")
    axs1[2].bar(br2, np.array(RMSE_all), width = barWidth, label = 'ALL')
    axs1[2].set_xticks(brn)
    axs1[2].set_xticklabels(model,rotation = 45,fontsize = font)
    axs1[2].tick_params(axis='y',labelsize = font)
    axs1[2].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs1[2].set_ylabel("RMSE",fontsize = font)
    axs1[2].set_ylim(0,1)
    
    figure1.suptitle("KPIs", fontsize = font)
    plt.tight_layout()
    plt.savefig(os.path.join('..',"Result Analysis","New models results","New_Models_KPI_test_on_diff_HPs.png"))
    plt.close()
    
    #Plot 2 SCOP
    figure2, axs2 = plt.subplots(1,figsize = (19,9.5))
      
    #Create barplot 2
    axs2.bar(br1, np.array(SCOP_mod_all), width = barWidth, label = "Model", color = "blue")
    axs2.bar(br2, np.array(SCOP_exp_stat), width = barWidth, label = 'Experimental - STAT', color = "orange", hatch='///')
    axs2.bar(br3, np.array(SCOP_exp_all), width = barWidth, label = 'Experimental - ALL',color = "orange")
    axs2.set_xticks(br2,model,fontsize = font)
    
    axs2.tick_params(axis='y',labelsize = font)
    axs2.set_xticks(brn)
    axs2.set_xticklabels(model,rotation = 45,fontsize = font)
    axs2.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    # axs2.set_ylabel("SCOP")
    axs2.legend(fontsize = font)    
    
    figure2.suptitle("SCOP",fontsize = font)
    plt.tight_layout()
    plt.savefig(os.path.join('..',"Result Analysis","New models results","SCOP_test_on_diff_HPs.png"))
    plt.close()

    #Create figures
    figure3, axs3 = plt.subplots(1,figsize = (19,9.5))

    #Select status
    Err_SCOP_mod_stat =  KPI.loc[KPI.index.get_level_values("status") == "STATIONARY","Err_SCOP [%]"]
    Err_SCOP_mod_mod =  KPI.loc[KPI.index.get_level_values("status") == "MODULATION","Err_SCOP [%]"]
    Err_SCOP_mod_def =  KPI.loc[KPI.index.get_level_values("status") == "MOD + DEF","Err_SCOP [%]"]
    Err_SCOP_mod_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","Err_SCOP [%]"]  
    
    barWidth = 0.2
    br1 = np.arange(len(Err_SCOP_mod_stat)) 
    br2 = [x + barWidth for x in br1] 
    br3 = [x + barWidth for x in br2] 
    br4 = [x + barWidth for x in br3] 
    brn = [x  for x in br2]
    
    #Create barplot 1 
    axs3.bar(br1, np.array(Err_SCOP_mod_stat ), width = barWidth, label = "STATIONARY",color="blue")
    axs3.bar(br2, np.array(Err_SCOP_mod_mod ), width = barWidth, label = "MODULATION",color = "green")
    axs3.bar(br3, np.array(Err_SCOP_mod_def ), width = barWidth, label = "MOD + DEF", color  ="purple")
    axs3.bar(br4, np.array(Err_SCOP_mod_all ), width = barWidth, label = "ALL",color  = "orange")
    axs3.set_xticks(brn)
    axs3.set_xticklabels(model,rotation = 45,fontsize = font)
    axs3.tick_params(axis='y',labelsize = font)
    axs3.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs3.set_ylabel("Err_SCOP [%]",fontsize = font)
    axs3.set_ylim(0,35)
    axs3.legend(fontsize = font)
    
    plt.tight_layout()
    plt.savefig(os.path.join('..',"Result Analysis","New models results","Err_SCOP_diff_HPs[%].png"))
    plt.close()

#%%%% Couples lists

devices = [  

            #10 kW        
            (("NIBE 2050 10 kW ID167 01-09-2024_30-04-2025","NIBE 2050 10 kW - DATA","AtW"),
            ("Riello NXHM 10 kW ID526 01-09-2024_30-04-2025","Riello NXHM 10 kW - DATA","AtW")),

            (("NIBE 2050 10 kW ID531 01-09-2024_30-04-2025","NIBE 2050 10 kW - DATA","AtW"),
            ("Riello NXHM 10 kW ID526 01-09-2024_30-04-2025","Riello NXHM 10 kW - DATA","AtW")),
            
            (("Riello NXHM 10 kW ID526 01-09-2024_30-04-2025","Riello NXHM 10 kW - DATA","AtW"),
            ("NIBE 2050 10 kW ID167 01-09-2024_30-04-2025","NIBE 2050 10 kW - DATA","AtW")),
            
            (("Riello NXHM 10 kW ID526 01-09-2024_30-04-2025","Riello NXHM 10 kW - DATA","AtW"),
            ("NIBE 2050 10 kW ID531 01-09-2024_30-04-2025","NIBE 2050 10 kW - DATA","AtW")),
            
            #16 kW
            (("NIBE F2040 16kW  ID288 01-09-2024_30-04-2025","NIBE F2040 16 kW - DATA","AtW"),
            ("LG Therma V 16kW  ID83 01-09-2024_30-04-2025","LG therma 16  kW - DATA ","AtW")),
            
            (("LG Therma V 16kW  ID83 01-09-2024_30-04-2025","LG therma 16  kW - DATA ","AtW"),
            ("NIBE F2040 16kW  ID288 01-09-2024_30-04-2025","NIBE F2040 16 kW - DATA","AtW")),
        
             ]

model = [
         "ID167 + ID526", 
         "ID531 + ID526",
         "ID526 + ID167", 
         "ID526 + ID531",
         "ID288 + ID83",
         "ID83 + ID288",
         ]

#%%Test on different machines

KPI = []  
for dev in devices: 

    HP1 = Heat_Pumps(dev[0])
    HP2 = Heat_Pumps(dev[1])
    
    #Status analysis and preparation of full load data
    HP1.status_analysis()
    HP1.interp_full_load()
    
    HP2.status_analysis()
    HP2.interp_full_load()
    
    #Regression on HP1
    HP1.new_model_fit_ML()
    HPC = Heat_Pumps_comparison(HP1,HP2)
    HPC.test_on_different_machines()
    KPI.append(HPC.KPI)

KPI = pd.concat(KPI)    
barplot(model,KPI, font = 12)



       