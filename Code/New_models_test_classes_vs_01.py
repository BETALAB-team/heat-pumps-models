import numpy as np
from New_models_classes_vs_01 import *
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt
#%% Set Seaborn theme
sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')

#%%Barplot
def barplot(model,KPI,font,k):

    #Create figures
    figure1, axs1 = plt.subplots(1,figsize = (19,9.5))
    
    R2_stat = KPI.loc[KPI.index.get_level_values("status") == "STEADY STATE","R2_Pow"]
    R2_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","R2_Pow"]  
    
    MAE_stat = KPI.loc[KPI.index.get_level_values("status") == "STEADY STATE","MAE_Pow"]
    MAE_mod =  KPI.loc[KPI.index.get_level_values("status") == "MODULATION","MAE_Pow"]
    MAE_mod_def =  KPI.loc[KPI.index.get_level_values("status") == "MOD + DEF","MAE_Pow"]
    MAE_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","MAE_Pow"]  
    
    cRMSE_stat = KPI.loc[KPI.index.get_level_values("status") == "STEADY STATE","cRMSE_Pow"]
    cRMSE_mod =  KPI.loc[KPI.index.get_level_values("status") == "MODULATION","cRMSE_Pow"]
    cRMSE_mod_def =  KPI.loc[KPI.index.get_level_values("status") == "MOD + DEF","cRMSE_Pow"]
    cRMSE_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","cRMSE_Pow"]  
    

    
    SCOP_mod_stat = KPI.loc[KPI.index.get_level_values("status") == "STEADY STATE","SCOP_model"]
    SCOP_exp_stat = KPI.loc[KPI.index.get_level_values("status") == "STEADY STATE","SCOP_exp"]
    
    SCOP_mod_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","SCOP_model"]  
    SCOP_exp_all =  KPI.loc[KPI.index.get_level_values("status") == "ALL","SCOP_exp"]  
    
    
    
    #Create bar
    barWidth = 0.4
    br1 = np.arange(len(R2_all)) 
    brn = [x + barWidth/2 for x in br1] 
    br2 = [x + barWidth for x in br1] 
    br3 = [x + barWidth for x in br2] 
    br4 = [x + barWidth for x in br3] 
    br5 = [x  for x in br2]
    
    #Create barplot 1 
    axs1.bar(br1, np.array(R2_stat), width = barWidth, label = "Steady-state")
    axs1.bar(br2, np.array(R2_all), width = barWidth, label = 'All operative conditions')
    axs1.set_xticks(brn,model, fontsize = font)
    axs1.tick_params(axis='y', labelsize = font)
    axs1.set_xticklabels(model,rotation = 90,fontsize = font)
    axs1.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs1.set_ylabel("R2 [-]", fontsize = font)
    axs1.set_ylim(0,1)
    # axs1.legend(fontsize = font)
    axs1.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), frameon = False, ncol = 2 ,fontsize = font)
    
    if k == 1:
        for i, tick in enumerate(axs1.get_xticklabels()):
            if i <= 7:  # solo i primi due
                tick.set_color("red")
            elif i >7 and i <=9:
               tick.set_color("blue")
            elif i >9 and i <=12:
               tick.set_color("purple")
            elif i == 13:
                tick.set_color("grey")
            elif i > 13 and i <= 19:
                tick.set_color("orange")
            elif i == 20:
                 tick.set_color("green")   
    elif k ==2:
        for i, tick in enumerate(axs1.get_xticklabels()):
            if i <= 7:  # solo i primi due
                tick.set_color("red")
            elif i >7 and i <=13:
               tick.set_color("orange")
      
             
    plt.tight_layout()
    # plt.savefig(os.path.join('..',"Result Analysis","New models results","New_Models_R2_sen.svg"))
    # plt.close()
    
#%% Plot 2 MAE
    figure2, axs2 = plt.subplots(1,figsize = (19,9.5))
    
    axs2.bar(br1, np.array(MAE_stat), width = barWidth, label = "Steady-State")
    # axs2.bar(br2, np.array(MPE_mod), width = barWidth, label = "MODULATION",color = "green")
    # axs2.bar(br3, np.array(MPE_mod_def), width = barWidth, label = "MOD + DEF", color  ="purple")
    axs2.bar(br2, np.array(MAE_all), width = barWidth, label = "All operative conditions")
    # axs2.legend(fontsize = font)
    axs2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), frameon = False, ncol = 2 , fontsize = font)
    
    axs2.set_xticks(br2,model,fontsize = font)
    axs2.tick_params(axis='y', labelsize = font)
    axs2.set_xticks(brn,model,fontsize = font)
    axs2.set_xticklabels(model,rotation = 90,fontsize = font)
    axs2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    axs2.set_ylabel("MAE [kW]",fontsize = font)
    
       
    if k == 1:
        for i, tick in enumerate(axs2.get_xticklabels()):
            if i <= 7:  # solo i primi due
                tick.set_color("red")
            elif i >7 and i <=9:
               tick.set_color("blue")
            elif i >9 and i <=12:
               tick.set_color("purple")
            elif i == 13:
                tick.set_color("grey")
            elif i > 13 and i <= 19:
                tick.set_color("orange")
            elif i == 20:
                 tick.set_color("green")   
    elif k ==2:
        for i, tick in enumerate(axs2.get_xticklabels()):
            if i <= 7:  # solo i primi due
                tick.set_color("red")
            elif i >7 and i <=13:
               tick.set_color("orange")
            
            
    plt.tight_layout()
    # plt.savefig(os.path.join('..',"Result Analysis","New models results","New_Models_MAE_sen.svg"))
    # plt.close()

#%%Plot 3 cRMSE
    
    figure2b, axs2b= plt.subplots(1,figsize = (19,9.5))
       
    axs2b.bar(br1, np.array(cRMSE_stat), width = barWidth, label = "Steady-State")
    # axs2b.bar(br2, np.array(RMSE_mod), width = barWidth, label = "MODULATION",color = "green")
    # axs2b.bar(br3, np.array(RMSE_mod_def), width = barWidth, label = "MOD + DEF", color  ="purple")
    axs2b.bar(br2, np.array(cRMSE_all), width = barWidth, label = 'All operative conditions')
    
    axs2b.set_xticks(br2,model,fontsize = font)
    axs2b.tick_params(axis='y',labelsize = font)
    axs2b.set_xticks(brn,model,fontsize = font)
    axs2b.set_xticklabels(model,rotation = 90,fontsize = font)
    axs2b.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs2b.set_ylabel("cRMSE [%]",fontsize = font)
    # axs2b.set_ylim(0,1)
    axs2b.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), frameon = False, ncol = 2 , fontsize = font)
    
        
    if k == 1:
        for i, tick in enumerate(axs2b.get_xticklabels()):
            if i <= 7:  # solo i primi due
                tick.set_color("red")
            elif i >7 and i <=9:
               tick.set_color("blue")
            elif i >9 and i <=12:
               tick.set_color("purple")
            elif i == 13:
                tick.set_color("grey")
            elif i > 13 and i <= 19:
                tick.set_color("orange")
            elif i == 20:
                 tick.set_color("green")   
    elif k ==2:
        for i, tick in enumerate(axs2b.get_xticklabels()):
            if i <= 7:  # solo i primi due
                tick.set_color("red")
            elif i >7 and i <=13:
               tick.set_color("orange")
      
    
    plt.tight_layout()
    # plt.savefig(os.path.join('..',"Result Analysis","New models results","New_Models_RMSE_sen.svg"))
    # plt.close()
   

#%% Scatter plot SCOP and Error
    figure4, axs4= plt.subplots(1,2,figsize = (19,9.5))
    
    if k == 1:
        #Marker 
        markers = ['o']*8 +['s']*2 +['^']*3+['D']*1+['o']*6+['v'] *1
        label = ["A05"]*8 + ["B10"]*2+["C10"]*3+["D12"]*1+["A12"]*6+["G11"]*1
        colors = ["red"]*8 +["blue"]*2+["purple"]*3+["grey"]*1+["orange"]*6+["green"]*1
        
    elif k == 2:
        #Marker 
        markers = ['o']*8 +['o']*6
        label = ["A05"]*8+["A12"]*6
        colors = ["red"]*8 +["orange"]*6
        
    y = np.array(SCOP_mod_stat)
    x = np.array(SCOP_exp_stat)
    y2 = np.array(SCOP_mod_all)
    x2 = np.array(SCOP_exp_all)
    
    added = set()
    for xi, yi, m,col in zip(x, y, markers,colors):
        if m not in added:
            axs4[0].scatter(xi, yi, marker=m, s=200, label=m,c= col,edgecolors= "black")
            added.add(m)
        else:
            axs4[0].scatter(xi, yi, marker=m, c = col,s=200,edgecolors= "black")

    axs4[0].plot([0, 10], [0, 10], "k--", label = "Bisector")
    axs4[0].plot([0, 10], [0, 11], "k--", label = "Error -20%")                    
    axs4[0].text( 5, 5.7, "+10%",fontsize = font)
    axs4[0].plot([0, 10], [0, 9], "k--", label = "Error +20%")
    axs4[0].text( 5, 4.7, "-10%",fontsize = font)
    axs4[0].set_xlim(3,6)
    axs4[0].set_ylim(3,6)
    axs4[0].set_xlabel("$SCOP_{exp,ss}$", fontsize = font)
    axs4[0].set_ylabel("$SCOP_{mod,ss}$",fontsize = font)
    axs4[0].tick_params(axis='y',labelsize = font)
    axs4[0].tick_params(axis='x',labelsize = font)
    
    added1 = set()
    for xi, yi, m,col in zip(x2, y2, markers,colors):
        if m not in added:
            axs4[1].scatter(xi, yi, marker=m, s=200, label=m,c = col,edgecolors= "black")
            added1.add(m)
        else:
            axs4[1].scatter(xi, yi, marker=m, c=col,s=200,edgecolors= "black")

    axs4[1].plot([0, 10], [0, 10], "k--", label = "Bisector")
    axs4[1].plot([0, 10], [0, 11], "k--", label = "Error -20%")                    
    axs4[1].text( 5, 5.7, "+10%",fontsize = font)
    axs4[1].plot([0, 10], [0, 9], "k--", label = "Error +20%")
    axs4[1].text( 5, 4.7, "-10%",fontsize = font)
    axs4[1].set_xlim(3,6)
    axs4[1].set_ylim(3,6)
    axs4[1].set_xlabel("$SCOP_{exp}$", fontsize = font)
    axs4[1].set_ylabel("$SCOP_{mod}$",fontsize = font)
    axs4[1].legend(fontsize=font)
    axs4[1].tick_params(axis='x',labelsize = font)
    axs4[1].tick_params(axis='y',labelsize = font)
    

    # Proxy legend
    if k == 1:
        legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='A05',
                   markerfacecolor='red', markersize=10, markeredgecolor='black'),
        plt.Line2D([0], [0], marker='s', color='w', label='B10',
                   markerfacecolor='blue', markersize=10, markeredgecolor='black'),
        plt.Line2D([0], [0], marker='^', color='w', label='C10',
                   markerfacecolor='purple', markersize=10, markeredgecolor='black'),
        plt.Line2D([0], [0], marker='D', color='w', label='D12',
                   markerfacecolor='grey', markersize=10, markeredgecolor='black'),
        plt.Line2D([0], [0], marker='o', color='w', label='A12',
                   markerfacecolor='orange', markersize=10, markeredgecolor='black'),
        plt.Line2D([0], [0], marker='v', color='w', label='G11',
                   markerfacecolor='green', markersize=10, markeredgecolor='black'),
        # Reference lines
        plt.Line2D([0,1], [0,1], color='k', linestyle='--', label='Bisector'),
        plt.Line2D([0,1], [0,1], color='k', linestyle='--', label='Error -10%'),
        plt.Line2D([0,1], [0,1], color='k', linestyle='--', label='Error +10%')
         ]
           
    
    elif k ==2:
        legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='A05',
                   markerfacecolor='red', markersize=10, markeredgecolor='black'),
        plt.Line2D([0], [0], marker='o', color='w', label='A12',
                   markerfacecolor='orange', markersize=10, markeredgecolor='black'),
        
        # Reference lines
        plt.Line2D([0,1], [0,1], color='k', linestyle='--', label='Bisector'),
        plt.Line2D([0,1], [0,1], color='k', linestyle='--', label='Error -10%'),
        plt.Line2D([0,1], [0,1], color='k', linestyle='--', label='Error +10%')
        ]
         

    # Aggiungi la legenda al subplot
    axs4[1].legend(handles=legend_elements, fontsize=font)
    

    plt.tight_layout()
    # plt.savefig(os.path.join('..',"Result Analysis","New models results","SCOP_sen.svg"))
    # plt.close()

#%% Devices lists and tests - catalogues

devices = [ #5kW
           # ("Valliant A+ 5kW ID9 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           # ("Valliant A+ 5kW ID24 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           # ("Valliant A+ 5kW ID33 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           # ("Valliant A+ 5kW ID77 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           # ("Valliant A+ 5kW ID78 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           # ("Valliant A+ 5kW ID115 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           # ("Valliant A+ 5kW ID151 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           # ("Valliant A+ 5kW ID227 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           
           #  # 10 kW
           # ("Riello NXHM 10 kW ID458 01-09-2024_30-04-2025","Riello NXHM 10 kW - DATA","AtW"),
           # ("Riello NXHM 10 kW ID526 01-09-2024_30-04-2025","Riello NXHM 10 kW - DATA","AtW"),
           # ("NIBE 2050 10 kW ID167 01-09-2024_30-04-2025","NIBE 2050 10 kW - DATA","AtW"),
           # ("NIBE 2050 10 kW ID531 01-09-2024_30-04-2025","NIBE 2050 10 kW - DATA","AtW"),
           # ("NIBE 2050 10 kW ID249 01-09-2024_30-04-2025","NIBE 2050 10 kW - DATA","AtW"),
           
           # # 12 kW
           # ("NIBE F2040 12 kW ID61 01-09-2024_30-04-2025","NIBE F2040 12 kW - DATA","AtW"),
           # ("Valliant A+ 12kW ID196 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW"),
           # ("Valliant A+ 12kW ID208 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW"),
           # ("Valliant A+ 12kW ID277 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW"),
           # ("Valliant A+ 12kW ID281 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW"),
           # ("Valliant A+ 12kW ID305 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW"),
           # ("Valliant A+ 12kW ID477 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW"),
           
           # # GeoT
           ("EcoGEO B1-9 11 kW ID571 01-09-2024_30-04-2025","EcoGEO B1-9 11 kW- DATA","WtW")
           ]

model = [
        # "VA+ 5 kW ID9", 
        #  "VA+ 5 kW ID24",
        #  "VA+ 5 kW ID33",
        #  "VA+ 5 kW ID77",
        #  "VA+ 5 kW ID78",
        #  "VA+ 5 kW ID115",
        #  "VA+ 5 kW ID151",
        #  "VA+ 5 kW ID227",
        #  "R_NXHM 10 kW ID458",
        #  "R_NXHM 10 kW ID526",
        #  "N F2050 10 kW ID167",
        #  "N F2050 10 kW ID531",
        #  "N F2050 10 kW ID249",
        #  "N F2040 12 kW ID61",
        #  "VA+ 12 kW ID196",
        #  "VA+ 12 kWI D208",
        #  "VA+ 12 kW ID277",
        #  "VA+ 12 kW ID281",
        #  "VA+ 12 kW ID305",
        #  "VA+ 12 kW ID477",
        #  "EG BC1/9 12 kW ID571"
        
        "A05I01",
        "A05I02",
        "A05I03",
        "A05I05",
        "A05I06",
        "A05I07",
        "A05I08",
        "A05I12",
        
        "B10I17",
        "B10I19",
        "C10I09",
        "C10I20",
        "C10I13",
        
        "D12I04",
        "A12I10",
        "A12I11",
        "A12I14",
        "A12I15",
        "A12I16",
        "A12I18",
        
        "G11I21",
         ]

#For loop
KPIs = [] 
for dev in devices:
    
    HP = Heat_Pumps(dev)
    HP.status_analysis()
    # HP.plot_test("2025-01-10 00:00:00","2025-01-11 00:00:00",20 )
    # HP.plot_test("2025-01-28 00:00:00","2025-01-29 00:00:00",20 )
    

    #Modelling
    HP.interp_full_load()
    HP.new_model_fit()
     

    #Plots
    # HP.plt_hist()
    # HP.function_plot()
    # HP.function_plot_2()
    # HP.envelope_plot()
    # df = HP.plot_full_load()
    # HP.plot_power_ratio()
    # P,S = HP.Selectbest()
    # HP.plot_time_series("2025-01-10 00:00:00","2025-01-11 00:00:00",20 )
    # HP.plot_time_series("2025-01-28 00:00:00","2025-01-29 00:00:00",20 )
    
    #Counter
    HC =np.array(HP.test["Heat Cap COND [kW]"])
    za = (HC >19).sum()
    
KPIs = pd.concat(KPIs)
# KPIs.to_csv(os.path.join('..',"Result Analysis","New models results","KPIs_sen.csv"))
# barplot(model,KPIs,20,1)



        
        
        
