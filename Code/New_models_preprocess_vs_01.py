import os 
import pandas as pd
import numpy as np
import pwlf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error, root_mean_squared_error,r2_score,mean_absolute_percentage_error

#%%Methods-Plots

def plot_power_vs_variables(exp,dev,var, HC_pred, Pow_pred, COP_pred):
    
    figure1, axs1 = plt.subplots(1,3, figsize = (19,9.5))
    sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
    
    
    #HC plot
    axs1[0].scatter(np.array(exp[f"{var}"]),np.array(exp["Heat Cap COND [kW]"]),label = "Exp Data")
    axs1[0].scatter(np.array(exp[f"{var}"]),np.array(HC_pred), label = "model")
    axs1[0].set_xlabel(f"{var}")
    axs1[0].set_ylabel("Heat Cap COND [kW]")
    axs1[0].legend()
    
    #Power plot
    axs1[1].scatter(np.array(exp[f"{var}"]),np.array(exp["Pow [kW]"]),label = "Exp Data")
    axs1[1].scatter(np.array(exp[f"{var}"]),np.array(Pow_pred), label = "model")
    axs1[1].set_xlabel(f"{var}")
    axs1[1].set_ylabel("Pow [kW]")
    axs1[1].legend()
    
    #COP plot
    axs1[2].scatter(np.array(exp[f"{var}"]),np.array(exp["COP"]),label = "Exp Data")
    axs1[2].scatter(np.array(exp[f"{var}"]),np.array(COP_pred), label = "model")
    axs1[2].set_xlabel(f"{var}")
    axs1[2].set_ylabel("COP")
    axs1[2].legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join('..',"Results",f"{dev}","New_models","Plot_NEW_MODEL_Power_vs_{var}.png"))
    plt.close()
    
    return

def plot_power_model(exp,dev, Pow_pred,status):
    
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

    plt.scatter(np.array(exp["Pow [kW]"]),Pow_pred, c = exp["PLR"], cmap='jet', label = "Power_model")
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
    plt.savefig(os.path.join('..',"Results",f"{dev}","New_models",f"NEW_MODEL_{status}.png"))
    plt.close()

#Color status plot
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

#Single day plot
def single_day_plot(data,start_date,end_date):
    figure1, axs1 = plt.subplots(1,figsize = (19,9.5))
    sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
    plt.tight_layout()
    
    data['Time'] = pd.to_datetime(data['Time'], unit='s')    
    filtered_data = data.loc[data["Time"] >= start_date]
    filtered_data = filtered_data.loc[filtered_data["Time"] <= end_date]
    x_data = np.array(filtered_data["Time"]) - pd.Timedelta(minutes = 2.5)
    
    axs1.set_title('HC and Pow')
    axs1.plot(np.array(filtered_data["Time"]) ,np.array(filtered_data["Heat Cap COND [kW]"]), label = "Heat capacity [kW]")
    plot_state_as_color(x_data, state_data=np.array(filtered_data["Status"]), axis=axs1)
    axs1.plot(np.array(filtered_data["Time"]),np.array(filtered_data["Pow [kW]"]), label = "Power [kW]")
    axs1.set_xlabel("Time [hours]")
    
    axs2 = axs1.twinx() 
    axs2.plot(np.array(filtered_data["Time"]), np.array(filtered_data["LExT [°C]"]), label = "LExT [°C]", color = "red")
    axs2.plot(np.array(filtered_data["Time"]),np.array(filtered_data["LET [°C]"]), label = "LET [°C]", color = "green")
    axs2.plot(np.array(filtered_data["Time"]),np.array(filtered_data["SET [°C]"]), label = "SET [°C]", color = "blue")

    axs1.legend()
    axs2.legend()
    
#Plot COP ratio as PLR function
def COP_PLR_plot(test, COP_fl, PLR, dev, status):
    
    figure1, axs1 = plt.subplots(1,2,figsize = (19,9.5))
    sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
   
    
    #Calculate ratio
    COP_ratio = test["COP"]/COP_fl
    Pow_ratio = test["Pow [kW]"]/test["Pow full [kW]"]
    
    
    
    #Plot
    axs1[0].scatter(test["PLR"] ,COP_ratio,label = "experimental points")
    axs1[0].set_xlabel("PLR")
    axs1[0].set_ylabel("COP/COP_fl")
    axs1[0].set_ylim(0,2)
    axs1[0].legend()
    
    axs1[1].scatter(test["PLR"],Pow_ratio,label = "experimental points")
    axs1[1].set_xlabel("PLR")
    axs1[1].set_ylabel("Pow ratio")
    axs1[1].set_ylim(0,2)
    axs1[1].legend()
    
    plt.savefig(os.path.join('..',"Results",f"{dev}","New_models",f"COP_ratio_vs_PLR_{status}.png"))
    plt.close()
    

#%% Methods - Create excel
def create_excel(new_file_name,test,catalogue_data):
    
    setdata = pd.read_excel(os.path.join('..','Data', f"{catalogue_data}.xlsx"), sheet_name = "SetData")
    curve = pd.read_excel(os.path.join('..','Data', f"{catalogue_data}.xlsx"), sheet_name = "curve")
    
    with pd.ExcelWriter(
        os.path.join('..','Data',new_file_name + ".xlsx"),
        mode="a",
        engine="openpyxl",
        if_sheet_exists="replace",
    ) as writer:
        setdata.to_excel(writer, sheet_name = "SetData")
        curve.to_excel(writer, sheet_name = "curve")
        test.to_excel(writer, sheet_name = "Test")            

#%% Methods - Define status and interpolations

#Adding the status of the machine to the dataset
def status_analysis(test, HC_des, Pow_des):
    
    #Clean the dataset
    col = ["Time","Pow [kW]","Heat Cap COND [kW]", "LExT [°C]", "LET [°C]", "LFR [kg/s]","SET [°C]"]
    test.columns = col
    
    #Conversion units of measurement
    test['Heat Cap COND [kW]'] = test['Heat Cap COND [kW]']/1000 #trasform to kW
    test['Pow [kW]'] = test['Pow [kW]']/1000  #trasform to kW
    test["LFR [kg/s]"] = test["LFR [kg/s]"] / 3600 #Conversion from l/h to kg/s

    #Initilize status
    status = []
    
    #ON-OFF status
    p_thresh = 0.05*Pow_des #[kW] 5% of the full load power SET =-7°C and LExT = 35°C from catalogue
    for i in test.index:
        if test["Pow [kW]"].get(i) < p_thresh:
            status.append('OFF')
        else:
            status.append(0)
            
    #Define Gradient
    #Values equally spaced by a 5 minutes interval
    Grad_EL = np.gradient(test["Pow [kW]"], 5) #compute the gradient using the delta time of 5 minutes [kW/min]
    Grad_HC = np.gradient(test["Heat Cap COND [kW]"],5)  #compute the gradient using the delta time of 5 minutes [kW/min]
    Grad_SET = np.gradient(test["SET [°C]"],5)  #compute the gradient using the delta time of 5 minutes [kW/min]

    
    #START and STOP status
    for i in test.index:
        if status[i] == 0 and status[i-1] == 'OFF':
            status[i] = 'START'
        elif status[i] == 'OFF' and status[i-1] == 0:
            status[i] = 'STOP'
            
    #DHW and DEF Status
    DeltaT = test["LExT [°C]"] - test["LET [°C]"]
    for i in test.index:
        if test["LExT [°C]"].get(i) > 50: #Above 50°C the unit is producing DHW
            status[i] = 'DHW'
        if (DeltaT[i] < 1 and status[i] == 0) or (test["Heat Cap COND [kW]"].get(i) <0 and status[i] == 0):
            status[i] = 'DEF'
            
    #Modulation and steady state regime   
    for i in test.index:
        if status[i] == 0 and abs(Grad_HC[i]) <= 0.05 * HC_des:
            #10%  of the full load HC SET =-7°C and LExT = 35°C from catalogue
            status[i] = 'STATIONARY'
        elif status[i] == 0 and Grad_HC[i] > 0.05 * HC_des:
            status[i] = 'ACCELERATION'
        elif status[i] == 0 and Grad_HC[i] < -0.05 * HC_des: #kW/min
            status[i] = 'DECELERATION'
    
    test["Status"] = status
    return test        
    
    
# Interpolation for HC full load calculation
def interp_full_load(data, catalogue_data, SET_des = -7, LExT_des = 35, HC_des = 5.89, Pow_des = 2.89):
    
    train = pd.read_excel(os.path.join('..','Data',f"{catalogue_data}.xlsx"), sheet_name = "Full Load").astype(float)
    test =  data
    
    #Drop Nan values
    test = test[test["Pow [kW]"] != 0]
    test = test[test['Pow [kW]'].notna()]
    test = test[test['Heat Cap COND [kW]'].notna()]
    test = test[test['LExT [°C]'].notna()]
    test = test[test['LET [°C]'].notna()]
    test = test[test["SET [°C]"].notna()]
    # test = test[test["LFR [kg/s]"].notna()]
    
    
    #Get data train
    SET = np.array(train["SET [°C]"] + 273.15)
    SET_des = SET_des + 273.15  #Trasform to K
    LExT = np.array(train["LExT [°C]"] + 273.15)
    LExT = LExT_des + 273.15 #Trasform to K
    Delta1 = (LExT - SET)/(LExT_des - SET_des)
    Delta2 = Delta1**2
    
    #Get data test
    SET_exp = np.array(test["SET [°C]"] + 273.15)
    LExT_exp = np.array(test["LExT [°C]"] + 273.15)
    Delta1_exp = (LExT_exp - SET_exp)/(LExT_des - SET_des)
    Delta2_exp = np.array(Delta1_exp**2)
     
    #Create train and test models
    X_train_HC = np.column_stack((Delta1,Delta2))
    # X_train_HC = np.array(Delta1).reshape(-1, 1)
    Y_train_HC =  np.array(train['Heat Cap COND [kW]']/HC_des)
    X_test_HC = np.column_stack((Delta1_exp,Delta2_exp))
    # X_test_HC = np.array(Delta1_exp).reshape(-1, 1)
    
    X_train_Pow = np.column_stack((Delta1,Delta2))
    # X_train_Pow = np.array(Delta1).reshape(-1, 1)
    Y_train_Pow =  np.array(train['Pow [kW]']/Pow_des)
    X_test_Pow = np.column_stack((Delta1_exp,Delta2_exp))
    # X_test_Pow = np.array(Delta1_exp).reshape(-1, 1)
    
    #Create the linear model
    model_HC = linear_model.LinearRegression().fit(X_train_HC,Y_train_HC)
    HC_fl_model = model_HC.predict(X_test_HC)*HC_des
    
    model_Pow = linear_model.LinearRegression().fit(X_train_Pow,Y_train_Pow)
    Pow_fl_model = model_Pow.predict(X_test_Pow)*Pow_des
    
    PLR = test['Heat Cap COND [kW]']/HC_fl_model
    
    #Create dataframe
    test['PLR'] = PLR
    test["COP"] = test["Heat Cap COND [kW]"]/test["Pow [kW]"]
    test["Heat Cap COND full [kW]"] = HC_fl_model
    test["Pow full [kW]"] = Pow_fl_model
    
    #Adjust PLR
    for i in test.index.values:
        if test.loc[i,"PLR"] > 1:
            test.loc[i,"PLR"] = 1
        elif test.loc[i,"PLR"] < 0:
            test.loc[i,"PLR"] = 0
            
    return test       

#Define new model
def complete_excel(devices, catalogue_data_dev,SET_fl = -7 ,  LExT_fl = 35, HC_fl = 5.89, Pow_fl = 2.89, COP_fl = 2.7):           
    
    #Clear the data
    for dev in devices:
        
        #Import entire database for the specific device
        data = pd.read_excel(os.path.join('..','ExpData',f"{dev}.xlsx"), sheet_name = "Sheet1")
        data = data.loc[:, ~data.columns.str.contains('^Unnamed')] 

        #%Creation of databases
        test_exp = status_analysis(data,HC_fl,Pow_fl)
        test_exp = interp_full_load(test_exp,catalogue_data_dev,SET_fl, LExT_fl ,HC_fl)
        
        #Create excel
        create_excel(dev,test_exp,catalogue_data_dev) 
    
        
#%% Creation of the complete excel file
def main():
    devices_valliant = [
               "Valliant A+ 5kW  ID5 01-11-2022_28-02-2023",
               "Valliant A+ 5kW  ID9 01-11-2022_28-02-2023",
               "Valliant A+ 5kW  ID24 01-11-2022_28-02-2023"
               ]
    
    devices_riello = [
                      "Riello NXHM 10 kW ID458 01-11-2024_28-02-2025",
                      "Riello NXHM 10 kW ID526 01-11-2024_28-02-2025"
                      ]
    
    devices_nibe = [
                      "NIBE 2050 10 kW ID65 01-11-2024_28-02-2025",
                      "NIBE 2050 10 kW ID167 01-11-2024_28-02-2025",
                      "NIBE 2050 10 kW ID531 01-11-2024_28-02-2025"
                      ]
    devices_nibe_2 = [
                    "NIBE F2040 12 kW ID61 01-11-2024_28-02-2025"
                    ]
    
    #Excel creation
    complete_excel(devices_valliant,"Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA")
    complete_excel(devices_riello,"Riello NXHM 10 kW - DATA",SET_fl = -7, LExT_fl = 35, HC_fl = 8, Pow_fl = 2.62, COP_fl =3.1)
    complete_excel(devices_nibe,"NIBE 2050 10 kW - DATA",SET_fl = -7,LExT_fl = 35,HC_fl = 8.7, Pow_fl = 2.9,COP_fl = 3)
    complete_excel(devices_nibe_2,"NIBE F2040 12 kW - DATA",SET_fl = -7,LExT_fl = 35,HC_fl = 10.3, Pow_fl = 3.73 ,COP_fl = 2.76)
    
#Run main
if __name__ == '__main__':
    main()
    

# KPI_all = pd.concat([KPI_all_val ,KPI_all_riello, KPI_all_nibe_2050])
# KPI_all.to_csv(os.path.join('..',"Result Analysis","KPI_new_model_2.csv"))

#Plot one single day
# single_day_plot(test_exp_nibe,"2024-12-12 00:00:00","2024-12-30 00:00:00" )

# KPI_short_val = new_model(devices_valliant, "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA",1)
# KPI_short = pd.concat(KPI_all_val ,KPI_all_midea)

# KPI_short.to_csv(os.path.join('..',"Result Analysis","KPI_new_model_short.csv"))



#%% Definition of a new correlation usign Pearson/ Kendall

#Create the test dataframe catalogue
# test_catalogue = {
#         "HC":Y1,
#         "Pow":Y2,
#         "COP": Y3,
#         "SET": SET,
#         "Delta": Delta1,
#         "LExT": LExT,
#         "PLR": PLR,
#         "SET^2": SET**2,
#         "Delta^2": Delta1**2,
#         "LExT^2": LExT**2,
#         "PLR^2": PLR**2,
#         "SET*LExT": SET*LExT,
#         "SET*Delta": SET*Delta1,
#         "LExT*Delta": LExT*Delta1,
#         "LExT*PLR": LExT*PLR,
#         "PLR*Delta": PLR*Delta1,
#         "SET*PLR": SET*PLR,
#         "SET^3":SET**3,
#         "SET^2*LExT":(SET**2)*LExT,
#         "SET^2*Delta":(SET**2)*Delta1,
#         "SET^2*PLR": (SET**2)*PLR,
#         "Delta^2*SET": (Delta1**2)*SET,
#         "Delta^3": Delta1**3,
#         "Delta^2*LExT": (Delta1**2)*LExT,
#         "Delta^2*PLR": (Delta1**2)*PLR,
#         "LExT^2*SET":(LExT**2)*SET,
#         "LExT^2*Delta":(LExT**2)*Delta1,
#         "LExT^3": LExT**3,
#         "LExT^2*PLR":(LExT**2)*PLR,
#         "PLR^2*SET": (PLR**2)*SET,
#         "PLR^2*Delta": (PLR**2)*Delta1,
#         "PLR^2*LExT": (PLR**2)*LExT,
#         "PLR^3":PLR**3
#         }

# #Create the test dataframe exp points
# test_exp = {
#         "HC":test_exp_val["Heat Cap COND [kW]"],
#         "Pow":test_exp_val["Pow [kW]"],
#         "COP": test_exp_val["COP"],
#         "SET": test_exp_val["SET [°C]"],
#         "LExT": test_exp_val["LExT [°C]"],
#         "Delta": test_exp_val["LExT [°C]"]- test_exp_val["SET [°C]"],
#         "PLR": test_exp_val ["PLR"],
#         # "SET^2": SET_test_exp_val**2,
#         "Delta^2": (test_exp_val["LExT [°C]"]- test_exp_val["SET [°C]"])**2,
#         # "LExT^2": LExT_test_exp_val**2,
#         # "PLR^2": PLR_test_exp_val**2,
#         # "SET*LExT": SET_test_exp_val*LExT_test_exp_val,
#         # "SET*Delta": SET_test_exp_val*Delta1_test_exp_val,
#         # "LExT*Delta": LExT_test_exp_val*Delta1_test_exp_val,
#         "LExT*PLR": test_exp_val["LExT [°C]"]*test_exp_val ["PLR"],
#         "PLR*Delta": test_exp_val ["PLR"]*(test_exp_val["LExT [°C]"]- test_exp_val["SET [°C]"]),
#         "SET*PLR": test_exp_val["SET [°C]"] * test_exp_val ["PLR"],
#         # "SET^3":SET_test_exp_val**3,
#         # "SET^2*LExT":(SET_test_exp_val**2)*LExT_test_exp_val,
#         # "SET^2*Delta":(SET_test_exp_val**2)*Delta1_test_exp_val,
#         # "SET^2*PLR": (SET_test_exp_val**2)*PLR_test_exp_val,
#         # "Delta^2*SET": (Delta1_test_exp_val**2)*SET_test_exp_val,
#         # "Delta^3": Delta1_test_exp_val**3,
#         # "Delta^2*LExT": (Delta1_test_exp_val**2)*LExT_test_exp_val,
#         "Delta^2*PLR": ((test_exp_val["LExT [°C]"]- test_exp_val["SET [°C]"])**2)*test_exp_val ["PLR"],
#         # "LExT^2*SET":(LExT_test_exp_val**2)*SET_test_exp_val,
#         # "LExT^2*Delta":(LExT_test_exp_val**2)*Delta1_test_exp_val,
#         # "LExT^3": LExT_test_exp_val**3,
#         # "LExT^2*PLR":(LExT_test_exp_val**2)*PLR_test_exp_val,
#         # "PLR^2*SET": (PLR_test_exp_val**2)*SET_test_exp_val,
#         # "PLR^2*Delta": (PLR_test_exp_val**2)*Delta1_test_exp_val,
#         # "PLR^2*LExT": (PLR_test_exp_val**2)*LExT_test_exp_val,
#         # "PLR^3":PLR_test_exp_val**3
#         }

# # test_cat = pd.DataFrame(test_catalogue)
# test_exp = pd.DataFrame(test_exp)

# # #Create correlation matrix
# # test_pearson_cat = test_cat.corr(method="pearson")
# # test_spearman_cat = test_cat.corr(method="spearman")

# test_pearson_exp = test_exp.corr(method="pearson")
# test_spearman_exp = test_exp.corr(method="spearman")
















