from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import MaxNLocator
import pandas as pd
import numpy as np
import seaborn as sns
import os
import matplotlib.pyplot as plt
#%% Set Seaborn theme
sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
#%%Barplot
def barplot(model,KPI,font,k):

    #Create figures
    figure1, axs1 = plt.subplots(1,figsize = (19,9.5))
    
    R2_stat = KPI.loc[KPI["status"] == "STEADY STATE","R2_Pow"]
    R2_all =  KPI.loc[KPI["status"] == "ALL","R2_Pow"]  
    
    MAE_stat = KPI.loc[KPI["status"] == "STEADY STATE","MAE_Pow"]
    MAE_all =  KPI.loc[KPI["status"] == "ALL","MAE_Pow"]  
    
    cRMSE_stat = KPI.loc[KPI["status"] == "STEADY STATE","cRMSE_Pow"]
    cRMSE_all =  KPI.loc[KPI["status"] == "ALL","cRMSE_Pow"]  
    
    
    SCOP_mod_stat = KPI.loc[KPI["status"] == "STEADY STATE","SCOP_model"]
    SCOP_exp_stat = KPI.loc[KPI["status"] == "STEADY STATE","SCOP_exp"]
    
    SCOP_mod_all =  KPI.loc[KPI["status"] == "ALL","SCOP_model"]  
    SCOP_exp_all =  KPI.loc[KPI["status"] == "ALL","SCOP_exp"]  
    
    
    
    #Create bar
    barWidth = 0.4
    br1 = np.arange(len(R2_all)) 
    brn = [x + barWidth/2 for x in br1] 
    br2 = [x + barWidth for x in br1] 
    br3 = [x + barWidth for x in br2] 
    br4 = [x + barWidth for x in br3] 
    br5 = [x  for x in br2]
    
    #Create barplot 1 
    axs1.bar(br1, np.array(R2_stat), width = barWidth, color = "#13315c",label = "Steady-state")
    axs1.bar(br2, np.array(R2_all), width = barWidth, color = "#d62828",label = 'All operative conditions')
    mean_stat = np.mean(R2_stat)
    mean_all = np.mean(R2_all)
    axs1.axhline(mean_stat, color="#012a4a", linestyle="--", label=f"$Mean_{{stat}}$ = {mean_stat:.2f}")
    axs1.axhline(mean_all, color= "#dc2f02", linestyle="--", label=f"$Mean_{{all}}$ = {mean_all:.2f}")
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
    plt.savefig(os.path.join('..',"Result Analysis","New models results","New_Models_R2_sen.svg"))
    plt.close()
    
#%% Plot 2 rMAE
    figure2, axs2 = plt.subplots(1,figsize = (19,9.5))
    
    axs2.bar(br1, np.array(MAE_stat), width = barWidth, color = "#13315c",label = "Steady-State")
    # axs2.bar(br2, np.array(MPE_mod), width = barWidth, label = "MODULATION",color = "green")
    # axs2.bar(br3, np.array(MPE_mod_def), width = barWidth, label = "MOD + DEF", color  ="purple")
    axs2.bar(br2, np.array(MAE_all), width = barWidth, color = "#d62828",label = "All operative conditions")
    mean_stat = np.mean(MAE_stat)
    mean_all = np.mean(MAE_all)
    axs2.axhline(mean_stat, color="#012a4a", linestyle="--", label=f"$Mean_{{stat}}$ = {mean_stat:.2f}")
    axs2.axhline(mean_all, color= "#dc2f02", linestyle="--", label=f"$Mean_{{all}}$ = {mean_all:.2f}")
    # axs2.legend(fontsize = font)
    axs2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), frameon = False, ncol = 2 , fontsize = font)
    
    axs2.set_xticks(br2,model,fontsize = font)
    axs2.tick_params(axis='y', labelsize = font)
    axs2.set_xticks(brn,model,fontsize = font)
    axs2.set_xticklabels(model,rotation = 90,fontsize = font)
    axs2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    axs2.set_ylabel("rMAE [%]",fontsize = font)
    
       
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
    plt.savefig(os.path.join('..',"Result Analysis","New models results","New_Models_rMAE_sen.svg"))
    plt.close()

#%%Plot 3 cRMSE
    
    figure2b, axs2b= plt.subplots(1,figsize = (19,9.5))
       
    axs2b.bar(br1, np.array(cRMSE_stat), width = barWidth,color = "#13315c", label = "Steady-State")
    # axs2b.bar(br2, np.array(RMSE_mod), width = barWidth, label = "MODULATION",color = "green")
    # axs2b.bar(br3, np.array(RMSE_mod_def), width = barWidth, label = "MOD + DEF", color  ="purple")
    axs2b.bar(br2, np.array(cRMSE_all), width = barWidth, color = "#d62828",label = 'All operative conditions')
    mean_stat = np.mean(cRMSE_stat)
    mean_all = np.mean(cRMSE_all)
    axs2b.axhline(mean_stat, color="#012a4a", linestyle="--", label=f"$Mean_{{stat}}$ = {mean_stat:.2f}")
    axs2b.axhline(mean_all, color= "#dc2f02", linestyle="--", label=f"$Mean_{{all}}$ = {mean_all:.2f}")
    
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
    plt.savefig(os.path.join('..',"Result Analysis","New models results","New_Models_cRMSE_sen.svg"))
    plt.close()
   

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
    # plt.savefig(os.path.join('..',"Result Analysis","New models results","SCOP.svg"))
    plt.close()
    
#%% Main
model = [
       
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

model1 = [
       
        "A05I01",
        "A05I02",
        "A05I03",
        "A05I05",
        "A05I06",
        "A05I07",
        "A05I08",
        "A05I12",
    
        "A12I10",
        "A12I11",
        "A12I14",
        "A12I15",
        "A12I16",
        "A12I18",

         ]



# KPIs = pd.read_csv(os.path.join('..',"Result Analysis","New models results","KPIs.csv"))
# barplot(model,KPIs,20,1)    

KPIs = pd.read_csv(os.path.join('..',"Result Analysis","New models results","KPIs_sen.csv"))
barplot(model1,KPIs,20,2)     
    
    
    
    
    