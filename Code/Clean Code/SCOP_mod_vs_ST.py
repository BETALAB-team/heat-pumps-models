from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import MaxNLocator
import pandas as pd
import numpy as np
import seaborn as sns
import os
import matplotlib.pyplot as plt

#%%#%% Set Seaborn theme and set working directory

sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
os.chdir('..')

#%%Barplot
def barplot(model,df,font):
    
    #Create figures
    figure1, axs1 = plt.subplots(1,figsize = (19,9.5))
    
    #Identify SCOP
    SCOP_st = df["Standard"].to_numpy()
    SCOP_exp = df["SCOP_EXP"].to_numpy()
    SCOP_mod = df["Mod"].to_numpy()
    
    #Create bars
    barWidth = 0.25
    br1 = np.arange(len(SCOP_st)) 
    br2 = [x + barWidth for x in br1] 
    br3 = [x + barWidth for x in br2] 

    #Create plots
    axs1.bar(br1, SCOP_exp, width = barWidth, color = "#13315c",edgecolor="black",label = "$SCOP_{exp}$")
    axs1.bar(br2, SCOP_st, width = barWidth, color = "#d8dcd6",edgecolor="black",label = "$SCOP_{st}$")
    axs1.bar(br3, SCOP_mod, width = barWidth, color = "#fac205",edgecolor="black",hatch ="\\",label = "$SCOP_{mod}$")

    axs1.set_xticks(br2,model, fontsize = font)
    axs1.tick_params(axis='y', labelsize = font)
    axs1.set_xticklabels(model,rotation = 90,fontsize = font)
    axs1.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    axs1.set_ylabel("SCOP [-]", fontsize = font)
    axs1.set_ylim(3,5.5)
    
    axs1.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), frameon = False, ncol = 3 ,fontsize = font)
    
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
  
             
    plt.tight_layout()
    # plt.savefig(os.path.join('..',"Result Analysis","New models results","Plot SCOP comparison steady state.svg"))
    plt.savefig(os.path.join('..',"Result Analysis","New models results","Plot SCOP comparison all.svg"))
    plt.close()
    
#%% SCOP comparison with Standard

df_steady = pd.read_excel(os.path.join('..',"Result Analysis","New models results","SCOP_st vs SCOP_mod.xlsx"), sheet_name = "SteadyState")
df_all = pd.read_excel(os.path.join('..',"Result Analysis","New models results","SCOP_st vs SCOP_mod.xlsx"), sheet_name = "All") 

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

#%Create barplot
# barplot(model,df_steady,20)
# barplot(model,df_all,20)
Err_st = abs(df_steady["Err_ST"]).mean()
Err_mod = abs(df_steady["Err_Mod"]).mean()
Err_st_all = abs(df_all["Err_ST"]).mean()
Err_mod_all = abs(df_all["Err_Mod"]).mean()