import numpy as np
from New_models_classes_vs_01 import *
from matplotlib.ticker import FormatStrFormatter
#%% Set Seaborn theme
sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')

#%%Barplot
#%%Barplot
def barplot(model,KPI,font):

    #Create figures
    figure1, axs1 = plt.subplots(1,figsize = (19,9.5))
    
    R2_stat = KPI.loc[KPI.index.get_level_values("status") == "STATIONARY","R2_Pow"]
    R2_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","R2_Pow"]  
    
    MPE_stat = KPI.loc[KPI.index.get_level_values("status") == "STATIONARY","MPE_Pow"]
    MPE_mod =  KPI.loc[KPI.index.get_level_values("status") == "MODULATION","MPE_Pow"]
    MPE_mod_def =  KPI.loc[KPI.index.get_level_values("status") == "MOD + DEF","MPE_Pow"]
    MPE_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","MPE_Pow"]  
    
    RMSE_stat = KPI.loc[KPI.index.get_level_values("status") == "STATIONARY","RMSE_Pow"]
    RMSE_mod =  KPI.loc[KPI.index.get_level_values("status") == "MODULATION","RMSE_Pow"]
    RMSE_mod_def =  KPI.loc[KPI.index.get_level_values("status") == "MOD + DEF","RMSE_Pow"]
    RMSE_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","RMSE_Pow"]  
    

    
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
    br4 = [x + barWidth for x in br3] 
    br5 = [x  for x in br2]
    
    #Create barplot 1 
    axs1.bar(br1, np.array(R2_stat), width = barWidth, label = "STATIONARY")
    axs1.bar(br2, np.array(R2_all), width = barWidth, label = 'ALL')
    axs1.set_xticks(brn,model, fontsize = font)
    axs1.tick_params(axis='y', labelsize = font)
    axs1.set_xticklabels(model,rotation = 90,fontsize = font)
    axs1.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs1.set_ylabel("R2", fontsize = font)
    axs1.set_ylim(0,1)
    axs1.legend(fontsize = font)
    
    plt.tight_layout()
    plt.savefig(os.path.join('..',"Result Analysis","New models results","New_Models_R2_exp.svg"))
    plt.close()
    
#%% Plot 2 MPE
    figure2, axs2 = plt.subplots(1,figsize = (19,9.5))
    
    axs2.bar(br1, np.array(MPE_stat), width = barWidth, label = "STATIONARY")
    # axs2.bar(br2, np.array(MPE_mod), width = barWidth, label = "MODULATION",color = "green")
    # axs2.bar(br3, np.array(MPE_mod_def), width = barWidth, label = "MOD + DEF", color  ="purple")
    axs2.bar(br2, np.array(MPE_all), width = barWidth, label = "ALL")
    axs2.legend(fontsize = font)
    
    axs2.set_xticks(br2,model,fontsize = font)
    axs2.tick_params(axis='y', labelsize = font)
    axs2.set_xticks(brn,model,fontsize = font)
    axs2.set_xticklabels(model,rotation = 90,fontsize = font)
    axs2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    axs2.set_ylabel("MPE",fontsize = font)
    
    plt.tight_layout()
    plt.savefig(os.path.join('..',"Result Analysis","New models results","New_Models_MPE_exp.svg"))
    plt.close()

#%%Plot 3 RMSE
    
    figure2b, axs2b= plt.subplots(1,figsize = (19,9.5))
       
    axs2b.bar(br1, np.array(RMSE_stat), width = barWidth, label = "STATIONARY")
    # axs2b.bar(br2, np.array(RMSE_mod), width = barWidth, label = "MODULATION",color = "green")
    # axs2b.bar(br3, np.array(RMSE_mod_def), width = barWidth, label = "MOD + DEF", color  ="purple")
    axs2b.bar(br2, np.array(RMSE_all), width = barWidth, label = 'ALL')
    
    axs2b.set_xticks(br2,model,fontsize = font)
    axs2b.tick_params(axis='y',labelsize = font)
    axs2b.set_xticks(brn,model,fontsize = font)
    axs2b.set_xticklabels(model,rotation = 90,fontsize = font)
    axs2b.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs2b.set_ylabel("RMSE",fontsize = font)
    axs2b.set_ylim(0,1)
    axs2b.legend(fontsize = font)
    
    plt.tight_layout()
    plt.savefig(os.path.join('..',"Result Analysis","New models results","New_Models_RMSE_exp.svg"))
    plt.close()
   
#%%#Plot  SCOP
    figure3, axs3 = plt.subplots(1,figsize = (19,9.5))
      
    #Create barplot 2
    # axs3.bar(br1, np.array(SCOP_mod_stat), width = barWidth, label = "Model", color = "blue",hatch='///')
    axs3.bar(br2, np.array(SCOP_exp_stat), width = barWidth, label = 'Experimental - STAT', color = "orange", hatch='///')
    axs3.bar(br1, np.array(SCOP_mod_all), width = barWidth, label = "Model", color = "blue")
    axs3.bar(br3, np.array(SCOP_exp_all), width = barWidth, label = 'Experimental - ALL',color = "orange")
    axs3.set_xticks(br2,model,fontsize = font)
    axs3.set_xticklabels(model,rotation = 90,fontsize = font)
    
    axs3.tick_params(axis='y',labelsize = font)
    axs3.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    # axs2.set_ylabel("SCOP")
    axs3.legend(fontsize = font)    
    
    figure3.suptitle("SCOP",fontsize = font)
    plt.tight_layout()
    plt.savefig(os.path.join('..',"Result Analysis","New models results","New_Models_SCOP_exp.svg"))
    plt.close()

#%%Err SCOP
    #Create figures
    figure4, axs4= plt.subplots(1,figsize = (19,9.5))

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
    axs4.bar(br1, np.array(Err_SCOP_mod_stat ), width = barWidth, label = "STATIONARY",color="blue")
    axs4.bar(br2, np.array(Err_SCOP_mod_mod ), width = barWidth, label = "MODULATION",color = "green")
    axs4.bar(br3, np.array(Err_SCOP_mod_def ), width = barWidth, label = "MOD + DEF", color  ="purple")
    axs4.bar(br4, np.array(Err_SCOP_mod_all ), width = barWidth, label = "ALL",color  = "orange")
    axs4.set_xticks(brn,model,fontsize = font)
    axs4.tick_params(axis='y',labelsize = font)
    axs4.set_xticklabels(model,rotation = 90,fontsize = font)
    axs4.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs4.set_ylabel("Err_SCOP [%]",fontsize = font)
    # axs4.set_ylim(-15,50)
    axs4.legend(fontsize = font)
    
    plt.tight_layout()
    plt.savefig(os.path.join('..',"Result Analysis","New models results","Err_SCOP_exp.svg"))
    plt.close()


    
#%% Devices lists and tests - Machin Learning
devices_ML = [
            #5 kW
          ("Valliant A+ 5kW ID9 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
          ("Valliant A+ 5kW ID24 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
          ("Valliant A+ 5kW ID33 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
          ("Valliant A+ 5kW ID77 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
          ("Valliant A+ 5kW ID78 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
          ("Valliant A+ 5kW ID115 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
          ("Valliant A+ 5kW ID151 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
          ("Valliant A+ 5kW ID227 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
          
          
          # # # # # #10 kW
          ("Riello NXHM 10 kW ID458 01-09-2024_30-04-2025","Riello NXHM 10 kW - DATA","AtW"),
          ("Riello NXHM 10 kW ID526 01-09-2024_30-04-2025","Riello NXHM 10 kW - DATA","AtW"),
          ("NIBE 2050 10 kW ID167 01-09-2024_30-04-2025","NIBE 2050 10 kW - DATA","AtW"),
          ("NIBE 2050 10 kW ID531 01-09-2024_30-04-2025","NIBE 2050 10 kW - DATA","AtW"),
          ("NIBE 2050 10 kW ID249 01-09-2024_30-04-2025","NIBE 2050 10 kW - DATA","AtW"),
          
          # # # # # #12 kW
          ("NIBE F2040 12 kW ID61 01-09-2024_30-04-2025","NIBE F2040 12 kW - DATA","AtW"),
          ("Valliant A+ 12kW ID196 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW"),
          ("Valliant A+ 12kW ID208 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW"),
          ("Valliant A+ 12kW ID277 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW"),
          ("Valliant A+ 12kW ID281 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW"),
          ("Valliant A+ 12kW ID305 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW"),
          ("Valliant A+ 12kW ID477 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW"),
           
           # #16 kW
           ("Midea MHC-V16 16kW  ID118 01-09-2024_30-04-2025","Midea MHC-V16  kW - DATA","AtW"),
           ("LG Therma V 16kW  ID83 01-09-2024_30-04-2025","LG therma 16  kW - DATA ","AtW"),
           ("NIBE F2040 16kW  ID288 01-09-2024_30-04-2025","NIBE F2040 16 kW - DATA","AtW"),
           
           #GeoT
           ("EcoGEO B1-9 11 kW ID571 01-09-2024_30-04-2025","EcoGEO B1-9 11 kW- DATA","WtW")
           ]

model = ["VA+ 5 kW ID9", 
         "VA+ 5 kW ID24",
         "VA+ 5 kW ID33",
         "VA+ 5 kW ID77",
         "VA+ 5 kW ID78",
         "VA+ 5 kW ID115",
         "VA+ 5 kW ID151",
         "VA+ 5 kW ID227",
         "R_NXHM 10 kW ID526",
         "R_NXHM 10 kW ID428",
         "N 2050 10 kW ID167",
         "N 2050 10 kW ID531",
         "N 2050 10 kW ID249",
         "N F2040 10 kW ID61",
         "VA+ 12 kW ID196",
         "VA+ 12 kWI D208",
         "VA+ 12 kW ID277",
         "VA+ 12 kW ID281",
         "VA+ 12 kW ID305",
         "VA+ 12 kW ID477",
         "MHC-V16 16kW  ID118",
         "LG TV  16 kW ID83",
         "N F2040 16 kW ID288",
         "EG BC1/9 12 kW ID571", 
         ]
    

KPIs_ML = []
SF = []
for dev in devices_ML:
    
    HP = Heat_Pumps(dev)
    HP.status_analysis()
    HP.interp_full_load()
    HP.new_model_fit_ML()
    KPIs_ML.append(HP.KPI_ML)
    
    # HP.plot_test("2024-12-01 00:00:00","2024-12-31 00:00:00" )
    # HP.envelope_plot() 

    
KPIs_ML = pd.concat(KPIs_ML)
barplot(model,KPIs_ML,12)
