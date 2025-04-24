
import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error, root_mean_squared_error,r2_score,mean_absolute_percentage_error
from sklearn.feature_selection import RFECV
from sklearn.svm import SVR

#%%Methods

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

def plot_power_model(exp,dev, Pow_pred, short_catalogue, equation_number,status):
    
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
    plt.xlim(0,3)
    plt.ylim(0,3)
    plt.ylabel('Power_model[kW]')
    plt.legend()
    
    # plt.tight_layout()
    if short_catalogue == 0:
        plt.savefig(os.path.join('..',"Results",f"{dev}","New_models",f"NEW_MODEL_{status}_eq_{equation_number}.png"))
    else:
        plt.savefig(os.path.join('..',"Results",f"{dev}","New_models",f"NEW_MODEL_{status}_eq_{equation_number}_SHORT.png"))
    plt.close()


#Adding the status of the machine to the dataset
def status_analysis(test):
    
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
    p_thresh = 0.05*2.18 #[kW] 5% of the full load power SET =-7°C and LExT = 35°C from catalogue
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
    DeltaT = test["LExT [°C]"] - test["SET [°C]"]
    for i in test.index:
        if test["LExT [°C]"].get(i) > 50: #Above 50°C the unit is producing DHW
            status[i] = 'DHW'
        if (DeltaT[i] < 1 and status[i] == 0) or (test["Heat Cap COND [kW]"].get(i) <0 and status[i] == 0):
            status[i] = 'DEF'
            
    #Modulation and steady state regime   
    for i in test.index:
        if status[i] == 0 and abs(Grad_HC[i]) <= 0.05 * 5.89:
            #10%  of the full load HC SET =-7°C and LExT = 35°C from catalogue
            status[i] = 'STATIONARY'
        elif status[i] == 0 and Grad_HC[i] > 0.05 * 5.89:
            status[i] = 'ACCELERATION'
        elif status[i] == 0 and Grad_HC[i] < -0.05 * 5.89: #kW/min
            status[i] = 'DECELERATION'
    
    test["Status"] = status
    return test        
    
    
# Interpolation for HC full load calculation
def interp_full_load(data, SET_des = -7, LExT_des = 35, HC_des = 5.89):
    
    train = pd.read_excel(os.path.join('..','ExpData',"HC_full.xlsx"), sheet_name = "HC full").astype(float)
    test =  data
    
    #Drop Nan values
    test = test[test["Pow [kW]"] != 0]
    test = test[test['Pow [kW]'].notna()]
    test = test[test['Heat Cap COND [kW]'].notna()]
    test = test[test['LExT [°C]'].notna()]
    test = test[test['LET [°C]'].notna()]
    test = test[test["SET [°C]"].notna()]
    test = test[test["LFR [kg/s]"].notna()]
    
    
    #Get data train
    SET = np.array(train["SET [°C]"]/SET_des)
    LExT = np.array(train["LExT [°C]"]/LExT_des)
    LET = np.array(train["LET [°C]"])
    Delta1 = (LExT - SET)/(LExT_des - SET_des)
    Delta2 = Delta1**2
    
    #Get data test
    SET_exp = np.array(test["SET [°C]"]/SET_des) #°C
    LExT_exp = np.array(test["LExT [°C]"]/LExT_des) #°C
    LET_exp = np.array(test["LET [°C]"])
    Delta1_exp = (LExT_exp - SET_exp)/(LExT_des - SET_des)
    Delta2_exp = np.array(Delta1_exp**2)
    
    #Create train and test models
    X_train = np.column_stack((SET,Delta1,Delta2))
    # X_train = np.column_stack((SET,LET,SET*LET))
    Y_train =  np.array(train['HC [kW]']/HC_des)
    X_test = np.column_stack((SET_exp,Delta1_exp,Delta2_exp))
    # X_test = np.column_stack((SET_exp,LET_exp,SET_exp*LET_exp))

    #Create the linear model
    model = linear_model.LinearRegression().fit(X_train,Y_train)
    HC_fl_model = model.predict(X_test)*HC_des
    PLR = test['Heat Cap COND [kW]']/HC_fl_model
    
    #Create dataframe
    test['PLR'] = PLR
    test["COP"] = test["Heat Cap COND [kW]"]/test["Pow [kW]"]
    test["Heat Cap COND full [kW]"] = HC_fl_model
    
    #Adjust PLR
    for i in test.index.values:
        if test.loc[i,"PLR"] > 1:
            test.loc[i,"PLR"] = 1
        elif test.loc[i,"PLR"] < 0:
            test.loc[i,"PLR"] = 0
    
    #Filter
    # test = test[abs(test['PLR']) == 1]
    # test = test[abs(test['PLR']) >= 0]
    
    return test       


def new_model(devices, short_catalogue = 0):        

    KPI = {}
    col = ["R2_Pow","MAPE_Pow","RMSE_Pow","SCOP_model","SCOP_exp","Err_SCOP"]
    states = ["STATIONARY","MODULATION","MOD + DEF","ALL"]
    multindex = [devices,states]
    multindex = pd.MultiIndex.from_product(multindex, names = ["model","status"])
    KPI = pd.DataFrame(KPI,index = multindex,columns = col)
    
    
    #Clear the data
    for dev in devices:
        
        #Import entire database for the specific device
        data = pd.read_excel(os.path.join('..','ExpData',f"{dev}.xlsx"), sheet_name = "Sheet1")
        data = data.loc[:, ~data.columns.str.contains('^Unnamed')] 
    
    
        #Import the data cleared with the PLR calculation
        if short_catalogue == 0:
            catalogue_data =  pd.read_excel(os.path.join('..','Data',f"{dev}.xlsx"), sheet_name = "SetData")
        elif short_catalogue == 1:
            catalogue_data =  pd.read_excel(os.path.join('..','Data',"Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA.xlsx"), sheet_name = "SetData_Short")
        # catalogue_data = catalogue_data.loc[catalogue_data["PLR"] == 1]
        
        #%Creation of databases
        cat_data_HC_full = pd.read_excel(os.path.join('..','Data',"Valliant A+ 5kW  ID24 01-11-2022_28-02-2023 HC_full.xlsx"), sheet_name = "HC full") 
        test_exp = status_analysis(data)
        test_exp = interp_full_load(test_exp)
        
        
        #Filter
        for i in range(4):
            if i == 0:
               exp = test_exp[test_exp['Status'] == 'STATIONARY']
            elif i == 1:
                exp = test_exp[(test_exp['Status'] == 'ACCELERATION') | (test_exp['Status'] == 'DECELERATION')
                          | (test_exp['Status'] == 'STATIONARY')]
            elif i == 2:
                exp = test_exp[(test_exp['Status'] == 'ACCELERATION') | (test_exp['Status'] == 'DECELERATION')
                          | (test_exp['Status'] == 'STATIONARY') | (test_exp['Status'] == 'DEF')]
            elif i == 3:
                exp = test_exp[(test_exp['Status'] == 'ACCELERATION') | (test_exp['Status'] == 'DECELERATION')
                          | (test_exp['Status'] == 'STATIONARY') | (test_exp['Status'] == 'DEF')  | (test_exp['Status'] == 'DHW')]
                
                figure1, axs1 = plt.subplots(1, figsize = (19,9.5))
                sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
                axs1.scatter(np.array(exp["Pow [kW]"]),np.array(exp["Heat Cap COND [kW]"]),label = "Exp Data")
           
            
              
            #Data in design conditions 
            SET_fl = -7 #°C
            LExT_fl = 35 #°C
            HC_fl = 5.89 # kW 
            COP_fl = 2.7 # kW
            Pow_fl = HC_fl/ COP_fl #kW
            PLR_fl = 1 #100% of load
            
            #Normalize the thermodynamics variables - Catalogues
            SET = catalogue_data["SET [°C]"]/SET_fl
            LExT =  catalogue_data["LExT [°C]"]/LExT_fl
            Delta1 = (catalogue_data["LExT [°C]"]-catalogue_data["SET [°C]"])/(LExT_fl - SET_fl)
            Delta2 = Delta1**2
            PLR =  catalogue_data["PLR"]
            
            # #Normalize the thermodinamics variables - Experimental Data
            SET_exp = exp["SET [°C]"]/SET_fl
            LExT_exp =  exp["LExT [°C]"]/LExT_fl
            Delta1_exp = (exp["LExT [°C]"]-exp["SET [°C]"])/(LExT_fl - SET_fl)
            Delta2_exp = Delta1_exp**2
            PLR_exp =  exp["PLR"]
            
            #Model input_-equation 1
            # X_train = np.column_stack((PLR,np.ones(len(PLR))))
            # X_test = np.column_stack((PLR_exp,np.ones(len(PLR_exp)))) 
            
            #Model input_-equation 2
            # X_train = np.column_stack((SET,Delta1,Delta2,PLR))
            # X_test = np.column_stack((SET_exp,Delta1_exp,Delta2_exp,PLR_exp))
            
            #Model input_- equation 3
            # X_train = np.column_stack((PLR*SET,PLR*Delta1,PLR*Delta2))
            # X_test = np.column_stack((PLR_exp*SET_exp,PLR_exp*Delta1_exp,PLR_exp*Delta2_exp))
            
            #Model input_- equation 4
            X_train = np.column_stack((PLR*SET,Delta1*PLR,LExT*PLR,PLR*Delta1**2))
            X_test = np.column_stack((PLR_exp*SET_exp,Delta1_exp*PLR_exp,LExT_exp*PLR_exp,PLR_exp*Delta1_exp**2))
            
            # X_train = np.column_stack((PLR,Delta1*PLR,LExT*PLR,PLR*Delta1**2,PLR*LExT**2,Delta1*PLR**2,LExT*PLR**2,PLR**2,PLR**3))
            # X_test = np.column_stack((PLR_exp,Delta1_exp*PLR_exp,LExT_exp*PLR_exp,PLR_exp*Delta1_exp**2,
                                # PLR_exp*LExT_exp**2,Delta1_exp*PLR_exp**2,LExT_exp*PLR_exp**2,PLR_exp**2,PLR_exp**3))
            
            Y1 = catalogue_data["Heat Cap COND [kW]"]/ HC_fl 
            Y2 = catalogue_data["Pow [kW]"]/Pow_fl
            Y3 = catalogue_data["COP"]/COP_fl
            
            #Model regression evaluation
            model_reg_HC = linear_model.LinearRegression(fit_intercept = False).fit(X_train, Y1)
            HC_pred = model_reg_HC.predict(X_test)*HC_fl
            
            model_reg_P = linear_model.LinearRegression(fit_intercept = False).fit(X_train, Y2)
            Pow_pred = model_reg_P.predict(X_test)*Pow_fl
            
            # model_reg_COP = linear_model.LinearRegression(fit_intercept = False).fit(X_train_COP, Y3)
            # COP_pred = model_reg_COP.predict(X_test_COP)*COP_fl
            
            COP_pred = exp["Heat Cap COND [kW]"]/Pow_pred
            
            #SCOP calculation
            SCOP_model = sum(np.array(exp["Heat Cap COND [kW]"]))/sum(Pow_pred)
            SCOP_exp = sum(np.array(exp["Heat Cap COND [kW]"]))/sum(np.array(exp["Pow [kW]"]))
        
            #KPI Calculations 
            if i == 0:
                KPI.loc[(dev,"STATIONARY"),"R2_Pow"] = float(r2_score(exp["Pow [kW]"],Pow_pred))
                KPI.loc[(dev,"STATIONARY"),"MAPE_Pow"] = float(mean_absolute_error(exp["Pow [kW]"],Pow_pred))
                KPI.loc[(dev,"STATIONARY"),"RMSE_Pow"] = float(root_mean_squared_error(exp["Pow [kW]"],Pow_pred).astype(float))
                
                  
                #SCOP
                KPI.loc[(dev,"STATIONARY"),"SCOP_model"] = float(SCOP_model.astype(float))
                KPI.loc[(dev,"STATIONARY"),"SCOP_exp"] = float(SCOP_exp.astype(float))
                KPI.loc[(dev,"STATIONARY"),"Err_SCOP"] = float(abs((SCOP_exp - SCOP_model)/SCOP_model))
                
                #Plot
                plot_power_model(exp, dev, Pow_pred, short_catalogue, 4,"STATIONARY")
    
            elif i == 1:
                KPI.loc[(dev,"MODULATION"),"R2_Pow"] = float(r2_score(exp["Pow [kW]"],Pow_pred))
                KPI.loc[(dev,"MODULATION"),"MAPE_Pow"] = float(mean_absolute_error(exp["Pow [kW]"],Pow_pred))
                KPI.loc[(dev,"MODULATION"),"RMSE_Pow"] = float(root_mean_squared_error(exp["Pow [kW]"],Pow_pred).astype(float))
                  
                #SCOP
                KPI.loc[(dev,"MODULATION"),"SCOP_model"] = float(SCOP_model.astype(float))
                KPI.loc[(dev,"MODULATION"),"SCOP_exp"] = float(SCOP_exp.astype(float))
                KPI.loc[(dev,"MODULATION"),"Err_SCOP"] = float(abs((SCOP_exp - SCOP_model)/SCOP_model))
                
                #Plot
                plot_power_model(exp,dev, Pow_pred,short_catalogue, 4,"MODULATION")
            
            elif i == 2:
                KPI.loc[(dev,"MOD + DEF"),"R2_Pow"] = float(r2_score(exp["Pow [kW]"],Pow_pred))
                KPI.loc[(dev,"MOD + DEF"),"MAPE_Pow"] = float(mean_absolute_error(exp["Pow [kW]"],Pow_pred))
                KPI.loc[(dev,"MOD + DEF"),"RMSE_Pow"] = float(root_mean_squared_error(exp["Pow [kW]"],Pow_pred).astype(float))
                  
                #SCOP
                KPI.loc[(dev,"MOD + DEF"),"SCOP_model"] = float(SCOP_model.astype(float))
                KPI.loc[(dev,"MOD + DEF"),"SCOP_exp"] = float(SCOP_exp.astype(float))
                KPI.loc[(dev,"MOD + DEF"),"Err_SCOP"] = float(abs((SCOP_exp - SCOP_model)/SCOP_model))
                
                #Plot
                plot_power_model(exp,dev, Pow_pred,short_catalogue, 4,"MOD + DEF")
                
            elif i == 3:
                KPI.loc[(dev,"ALL"),"R2_Pow"] = float(r2_score(exp["Pow [kW]"],Pow_pred))
                KPI.loc[(dev,"ALL"),"MAPE_Pow"] = float(mean_absolute_error(exp["Pow [kW]"],Pow_pred))
                KPI.loc[(dev,"ALL"),"RMSE_Pow"] = float(root_mean_squared_error(exp["Pow [kW]"],Pow_pred).astype(float))
                  
                #SCOP
                KPI.loc[(dev,"ALL"),"SCOP_model"] = float(SCOP_model.astype(float))
                KPI.loc[(dev,"ALL"),"SCOP_exp"] = float(SCOP_exp.astype(float))
                KPI.loc[(dev,"ALL"),"Err_SCOP"] = float(abs((SCOP_exp - SCOP_model)/SCOP_model))
                
                #Plot
                plot_power_model(exp,dev, Pow_pred, short_catalogue,4,"ALL") \
        
    return KPI

#%% New model creation and results
devices = [
           "Valliant A+ 5kW  ID5 01-11-2022_28-02-2023",
           "Valliant A+ 5kW  ID9 01-11-2022_28-02-2023",
           "Valliant A+ 5kW  ID24 01-11-2022_28-02-2023"
           ]

KPI_all = new_model(devices)
KPI_all.to_csv(os.path.join('..',"Result Analysis","KPI_new_model.csv"))
KPI_short = new_model(devices, short_catalogue = 1)
KPI_short.to_csv(os.path.join('..',"Result Analysis","KPI_new_model_short.csv"))



















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
#         "HC":exp["Heat Cap COND [kW]"],
#         "Pow":exp["Pow [kW]"],
#         "COP": exp["COP"],
#         "SET": SET_exp,
#         "Delta": Delta1_exp,
#         "LExT": LExT_exp,
#         "PLR": PLR_exp,
#         "SET^2": SET_exp**2,
#         "Delta^2": Delta1_exp**2,
#         "LExT^2": LExT_exp**2,
#         "PLR^2": PLR_exp**2,
#         "SET*LExT": SET_exp*LExT_exp,
#         "SET*Delta": SET_exp*Delta1_exp,
#         "LExT*Delta": LExT_exp*Delta1_exp,
#         "LExT*PLR": LExT_exp*PLR_exp,
#         "PLR*Delta": PLR_exp*Delta1_exp,
#         "SET*PLR": SET_exp*PLR_exp,
#         "SET^3":SET_exp**3,
#         "SET^2*LExT":(SET_exp**2)*LExT_exp,
#         "SET^2*Delta":(SET_exp**2)*Delta1_exp,
#         "SET^2*PLR": (SET_exp**2)*PLR_exp,
#         "Delta^2*SET": (Delta1_exp**2)*SET_exp,
#         "Delta^3": Delta1_exp**3,
#         "Delta^2*LExT": (Delta1_exp**2)*LExT_exp,
#         "Delta^2*PLR": (Delta1_exp**2)*PLR_exp,
#         "LExT^2*SET":(LExT_exp**2)*SET_exp,
#         "LExT^2*Delta":(LExT_exp**2)*Delta1_exp,
#         "LExT^3": LExT_exp**3,
#         "LExT^2*PLR":(LExT_exp**2)*PLR_exp,
#         "PLR^2*SET": (PLR_exp**2)*SET_exp,
#         "PLR^2*Delta": (PLR_exp**2)*Delta1_exp,
#         "PLR^2*LExT": (PLR_exp**2)*LExT_exp,
#         "PLR^3":PLR_exp**3
#         }

# test_cat = pd.DataFrame(test_catalogue)
# test_exp = pd.DataFrame(test_exp)

# #Create correlation matrix
# test_pearson_cat = test_cat.corr(method="pearson")
# test_spearman_cat = test_cat.corr(method="spearman")

# test_pearson_exp = test_exp.corr(method="pearson")
# test_spearman_exp = test_exp.corr(method="spearman")














