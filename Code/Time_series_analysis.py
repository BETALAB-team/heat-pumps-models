#Import
import os
import pandas as pd 
import numpy as np
from scipy.interpolate import LinearNDInterpolator
from scipy.signal import find_peaks, peak_prominences
from sklearn import linear_model
from sklearn.linear_model import Ridge, Lasso, ElasticNet
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import from_levels_and_colors
import datetime
from time import strftime,localtime

#%% Interpolation for HC full load calculation

def interp2D(file,data):
    train = pd.read_excel(os.path.join('..','ExpData',"HC_full.xlsx"), sheet_name = "HC full").astype(float)
    test =  data
    
    #Drop raw where Pel == 0 kW
    test = test[test['Pow [kW]'] != 0]
    
    #Get Data
    x = np.array(train["SET [°C]"])
    y = np.array(train["LExT [°C]"])
    z = np.array(train["HC [kW]"])
    w = np.array(train["COP"])
    
    
    X = np.array(test["SET [°C]"])
    Y= np.array(test["LExT [°C]"])
    HC = np.array(test["Heat Cap COND [kW]"])

    #Interpolate
    interp = LinearNDInterpolator(list(zip(x, y)), z)
    interp2 = LinearNDInterpolator(list(zip(x, y)), w)
    
    Z = interp(X,Y)
    PLR = HC/Z
    COP_full = interp2(X,Y)
    
    
    #Create dataframe
    test['PLR'] = PLR
    test["Heat Cap COND full [kW]"] = Z
    test['Pow full [kW]'] = Z/COP_full
    test['COP_full'] = COP_full

    #Clean dataframe 
    test = test[test['PLR'].notna()]
    test = test[test['COP_full'].notna()]
    test = test[test['Pow [kW]'].notna()]
    test = test[test['Pow [kW]'].notna()]
    test = test[abs(test['PLR']) <= 1]
    
    return test
        
#%% Create Excel
def create_excel(file,new_file_name,res):
    
    SetData = pd.read_excel(os.path.join('..','Data',f"{file} - DATA.xlsx"), sheet_name = "SetData",).astype(float) 
    Curve = pd.read_excel(os.path.join('..','Data', f"{file} - DATA.xlsx"), sheet_name = "curve",)
    
    with pd.ExcelWriter(
        os.path.join('..','Data',new_file_name + ".xlsx"),
        mode="a",
        engine="openpyxl",
        if_sheet_exists="replace",
    ) as writer:
        SetData.to_excel(writer, sheet_name = "SetData")
        Curve.to_excel(writer, sheet_name = "curve")
        res.to_excel(writer, sheet_name = "Test")

#%% background plot color

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
                
#%%Input variables
devices = [
           # "Valliant A+ 5kW  ID5 01-11-2022_28-02-2023",
           "Valliant A+ 5kW  ID9 01-11-2022_28-02-2023",
           # "Valliant A+ 5kW  ID24 01-11-2022_28-02-2023"
           ]

#Clear the data
for dev in devices:
    data = pd.read_excel(os.path.join('..','ExpData',f"{dev}.xlsx"), sheet_name = "Sheet1")
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')] 
    col = ["Time","Pow [kW]","Heat Cap COND [kW]", "LExT [°C]", "LET [°C]", "LFR [kg/s]","SET [°C]"]
    data.columns = col
    data["Pow [kW]"] = data["Pow [kW]"]/1000
    data["Heat Cap COND [kW]"] = data["Heat Cap COND [kW]"]/1000
    data["LFR [kg/s]"] =  data["LFR [kg/s]"]/3600 #Conversion from l/h to kg/s
    
    #COP calculation
    COP = data["Heat Cap COND [kW]"]/ data["Pow [kW]"]

    #Time series analysis Defrost
    DeltaT = data['LExT [°C]'] - data['SET [°C]'] 
    DeltaT2 = DeltaT**2
    
    #Initilize status
    status = []
    
    #ON-OFF status
    p_thresh = 0.05*2.18 #[kW] 5% of the full load power SET =-7°C and LExT = 35°C from catalogue
    for i in data.index:
        if data["Pow [kW]"].get(i) < p_thresh:
            status.append('OFF')
        else:
            status.append(0)
            
    #Define Gradient
    #Values equally spaced by a 5 minutes interval
    Grad_EL = np.gradient( data["Pow [kW]"], 5) #compute the gradient using the delta time of 5 minutes [kW/min]
    Grad_HC = np.gradient( data["Heat Cap COND [kW]"],5)  #compute the gradient using the delta time of 5 minutes [kW/min]
    Grad_SET = np.gradient( data["SET [°C]"],5)  #compute the gradient using the delta time of 5 minutes [kW/min]

    
    #START and STOP status
    for i in data.index:
        if status[i] == 0 and status[i-1] == 'OFF':
            status[i] = 'START'
        elif status[i] == 'OFF' and status[i-1] == 0:
            status[i] = 'STOP'
            
    #DHW and DEF Status
    for i in data.index:
        if data["LExT [°C]"].get(i) > 50: #Above 50°C the unit is producing DHW
            status[i] = 'DHW'
        if (DeltaT[i] < 1 and status[i] == 0) or (data["Heat Cap COND [kW]"].get(i) <0 and status[i] == 0):
            #Assumed DeltaT < 1 for defrost status according to uncertanty of measurement
            status[i] = 'DEF'
            
    #Modulation status
    # for i in data.index:
    #     if status[i] == 0 and abs(Grad_EL[i]) <= 0.033 and abs(Grad_HC[i]) <= 0.1: 
    #     # if status[i] == 0 and abs(Grad_HC[i]) <= 0.05:
    #         status[i] = 'STATIONARY'
    #     elif status[i] == 0 and Grad_EL[i] > 0.033:
    #         status[i] = 'ACCELERATION'
    #     elif status[i] == 0 and Grad_EL[i] < -0.033:
    #         status[i] = 'DECELERATION'
    #         if Grad_HC[i+1] < -0.1 and status[i+1] == 0:
    #             status[i+1]= 'DECELERATION'
    #             if Grad_HC[i+2] < -0.1 and status[i+2] == 0:
    #                 status[i+2]= 'DECELERATION'
    #                 i += 2
    #             i += 1
    #     elif status[i] == 0 and abs(Grad_HC[i]) > 0.1:
    #         status[i] = 'FLUCTUATIONS'
    
    #Finding maximum and minimum peaks of the HC
    # data["Status"] = status 
    # peaks, _ = find_peaks(data["Heat Cap COND [kW]"])
    # mins, _ = find_peaks(-data["Heat Cap COND [kW]"])
    # peaks_positions = []
    
    # for i in data.index:
    #     if i in peaks:
    #         peaks_positions.append(1)
    #     elif i in mins:
    #         peaks_positions.append(1)
    #     else:
    #         peaks_positions.append(0)
    

    # for p,m in zip(peaks,mins):
    #     mobile_window = data[p+1:m]
    #     for i in mobile_window.index:
    #         if status[i] == 0:
    #             status[i] = "ACCELERATION"  
    #Nan values (with error in calcuation of gradient)
    # for i in data.index:
    #     if status[i] == 0:
    #        status[i] = "ACCELERATION"

                  
           
        
    for i in data.index:
        if status[i] == 0 and abs(Grad_HC[i]) <= 0.05 * 5.89:
            #10%  of the full load HC SET =-7°C and LExT = 35°C from catalogue
            status[i] = 'STATIONARY'
        elif status[i] == 0 and Grad_HC[i] > 0.05 * 5.89:
            status[i] = 'ACCELERATION'
        elif status[i] == 0 and Grad_HC[i] < -0.05 * 5.89: #kW/min
            status[i] = 'DECELERATION'

   
    #add information to dataframe
    data["COP"] = COP
    data["Gradient EL"] = Grad_EL
    data["Gradient HC"] = Grad_HC
    data["Gradient SET"] = Grad_SET
    data["Delta"] = DeltaT
    data["Delta2"] = DeltaT2
    data["Status"] = status  
    # data["Peaks"] = peaks_positions
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')] 
    
    #Launch pre-processing
    res = interp2D(dev, data)
    
    #filter data
    # res = res[res['Status'] == 'STATIONARY']
    res = res[(res['Status'] == 'ACCELERATION') | (res['Status'] == 'DECELERATION')
              | (res['Status'] == 'STATIONARY')]
              # | (res['Status'] == 'TRANSITORY')]
    # res = res[(res['Status'] == 'ACCELERATION')]
    # res = res[res['Status'] == 'DECELERATION']
    # res = res[res['Status'] == 'FLUCTUATIONS']
    # res = res[res['Status'] == 'DEF']
    # res = res[res['Status'] == 'DHW']
    # res = res[res['Status'] == 'OFF']
    # res = res[res['Status'] == 'START']
    # res = res[res['Status'] == 'STOP']
    
    
    res.to_excel(os.path.join('..','Result Analysis','err gradient.xlsx'), index=False)
    create_excel("Valliant Aerotherm plus  VWL 55-6  A S3 5 kW", dev,res)
    
#%% Plot one single day

figure1, axs1 = plt.subplots(1,figsize = (19,9.5))
sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
plt.tight_layout()

data['Time'] = pd.to_datetime(data['Time'], unit='s')

start_date = "2022-12-12 00:00:00"
end_date = "2022-12-30 00:00:00" 

filtered_data = data.loc[data["Time"] >= start_date]
filtered_data = filtered_data.loc[filtered_data["Time"] <= end_date]
x_data = np.array(filtered_data["Time"]) - pd.Timedelta(minutes = 2.5)

axs1.set_title('HC and Pow')
axs1.plot(np.array(filtered_data["Time"]) ,np.array(filtered_data["Heat Cap COND [kW]"]), label = "Heat capacity [kW]")
plot_state_as_color(x_data, state_data=np.array(filtered_data["Status"]), axis=axs1)
axs1.plot(np.array(filtered_data["Time"]),np.array(filtered_data["Pow [kW]"]), label = "Power [kW]")
# axs1.plot(np.array(filtered_data["Time"]),np.array(filtered_data["Peaks"]*np.array(filtered_data["Heat Cap COND [kW]"])),"x", label = "Peaks")
axs1.set_xlabel("Time [hours]")

axs2 = axs1.twinx() 
axs2.plot(np.array(filtered_data["Time"]), np.array(filtered_data["LExT [°C]"]), label = "LExT [°C]", color = "red")
axs2.plot(np.array(filtered_data["Time"]),np.array(filtered_data["LET [°C]"]), label = "LET [°C]", color = "green")
# axs2.plot(np.array(filtered_data["Time"]),np.array(filtered_data["LFR [kg/s]"]), label = "LFR [kg/s]", color = "yellow")
axs2.plot(np.array(filtered_data["Time"]),np.array(filtered_data["SET [°C]"]), label = "SET [°C]", color = "blue")
axs2.plot(np.array(filtered_data["Time"]),np.array(filtered_data["Gradient EL"]), label = "Gradient EL", color = "red")
axs2.plot(np.array(filtered_data["Time"]),np.array(filtered_data["Gradient HC"]), label = "Gradient HC", color = "green")




axs1.legend()
axs2.legend()

status_time = {
            "stat_time": len(filtered_data.loc[filtered_data["Status"] == "STATIONARY"])*5/60,
            "decc_time":  len(filtered_data.loc[filtered_data["Status"] == "DECELERATION"])*5/60,
            "acc_time": len(filtered_data.loc[filtered_data["Status"] == "ACCELERATION"])*5/60,
            "def_time": len(filtered_data.loc[filtered_data["Status"] == "DEF"])*5/60,
            "dhw_time": len(filtered_data.loc[filtered_data["Status"] == "DHW"])*5/60,
            "start_time": len(filtered_data.loc[filtered_data["Status"] == "START"])*5/60,
            "stop_time": len(filtered_data.loc[filtered_data["Status"] == "STOP"])*5/60,
            "off_time": len(filtered_data.loc[filtered_data["Status"] == "OFF"])*5/60,
            "fluctuation_time": len(filtered_data.loc[filtered_data["Status"] == "FLUCTUATIONS"])*5/60,
            "NO INFO":  len(filtered_data.loc[filtered_data["Status"] == "NO INFO"])*5/60
            }
            
# print(sum(status_time.values()))         
# plt.close()
       
#%% Climatic curve

filtered_data1 = data[(data['Status'] == 'ACCELERATION') | (data['Status'] == 'DECELERATION')
          | (data['Status'] == 'STATIONARY')]

figure2, axs3 = plt.subplots(1,figsize = (19,9.5))
sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
plt.tight_layout()

axs3.set_title('Climatic Curve')
axs3.scatter(np.array(filtered_data1["SET [°C]"]) ,np.array(filtered_data1["LExT [°C]"]), label = "Climatic")
axs3.set_xlabel("SET [°C]")
axs3.set_ylabel("LExT [°C]")
plt.close()

#%% Plot powers as function of thermal variables of the machine

Filter = [
        'STATIONARY',
        'ACCELERATION',
        'DECELERATION'
        ]

variables = ["SET [°C]",
             "LExT [°C]",
             "Delta",
             ]


def plot_power_vs_variables(data, Filter, var, device):

    f_data = data.loc[data['Status'] == Filter ]
    
    figure4, axs4 = plt.subplots(1,2, figsize = (19,9.5))
    sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
    
    
    #HC and Power vs SET
    axs4[0].scatter(np.array(f_data[f"{var}"]),np.array(f_data["Heat Cap COND [kW]"]), c = "blue")
    # axs4[0].scatter(np.array(fil[f"{var}"]),np.array(HC_pred), c = "green")
    axs4[0].set_xlabel(f"{var}")
    axs4[0].set_ylabel("Heat Cap COND [kW]")
    
    
    axs4[1].scatter(np.array(f_data[f"{var}"]),np.array(f_data["Pow [kW]"]), c = "red")
    # axs4[1].scatter(np.array(fil[f"{var}"]),np.array(Pow_pred), c = "green")
    axs4[1].set_xlabel(f"{var}")
    axs4[1].set_ylabel("Pow [kW]")
    plt.tight_layout()
    plt.savefig(os.path.join('..',"Results",f"{dev}","Time_Series_Analysis",f"{Filter}_Plot_Power_vs_{var}.png"))
    plt.close()
    return

def plot_power_vs_variables_RES(data,Filter, var, device):

    f_data = data.loc[data['Status'] == Filter ]
    
    figure4, axs4 = plt.subplots(1,3, figsize = (19,9.5))
    sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')

    
    
    #HC and Power vs SET
    axs4[0].scatter(np.array(f_data[f"{var}"]),np.array(f_data["Heat Cap COND [kW]"]), c = f_data["PLR"], cmap='viridis')
    axs4[0].set_xlabel(f"{var}")
    axs4[0].set_ylabel("Heat Cap COND [kW]")
    
    
    axs4[1].scatter(np.array(f_data[f"{var}"]),np.array(f_data["Pow [kW]"]),c = f_data["PLR"], cmap='viridis')
    # axs4[1].scatter(np.array(fil[f"{var}"]),np.array(Pow_pred), c = "green")
    axs4[1].set_xlabel(f"{var}")
    axs4[1].set_ylabel("Pow [kW]")
    
    im2 = axs4[2].scatter(np.array(f_data[f"{var}"]),np.array(f_data["COP"]),c = f_data["PLR"], cmap='viridis')
    # axs4[1].scatter(np.array(fil[f"{var}"]),np.array(Pow_pred), c = "green")
    axs4[2].set_xlabel(f"{var}")
    axs4[2].set_ylabel("COP")
    
    # add the bar
    cbar = plt.colorbar(im2, orientation='vertical' )
    cbar.set_label("PLR")

    plt.tight_layout()
    plt.savefig(os.path.join('..',"Results",f"{dev}","Time_Series_Analysis",f"{Filter}_Plot_Power_vs_{var}_PLR.png"))
    plt.close()
    
    # assign plot to a new object



for f in Filter:
    for v in variables:
        for dev in devices:
            plot_power_vs_variables(data,f,v,dev)
            plot_power_vs_variables_RES(res,f,v,dev)



























































































            
            
            
            
            
            
            
            
            
         

