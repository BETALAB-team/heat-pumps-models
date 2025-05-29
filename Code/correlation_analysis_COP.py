import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pwlf
import math
from sklearn import linear_model
from sklearn.metrics import mean_absolute_error, root_mean_squared_error,r2_score,mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LassoCV
from sklearn.feature_selection import RFE
from sklearn.linear_model import BayesianRidge
# from gplearn.genetic import SymbolicRegressor
# from pysr import PySRRegressor
from scipy.optimize import curve_fit
from sklearn.preprocessing import StandardScaler
from sympy import *
#%% Methods

#Plot COP ratio as PLR function
def COP_Pow_PLR_plot(test,Pow_ratio_model):
    # figure1, axs1 = plt.subplots(1,2,figsize = (19,9.5))
    # sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
   
    
    COP_fl_model = test["Heat Cap COND full [kW]"]/ test["Pow full [kW]"]
    COP_ratio = test["COP"]/COP_fl_model
    Pow_ratio = test["Pow [kW]"]/test["Pow full [kW]"]
    Pow = test["Pow [kW]"]
    
    # #Plot
    # axs1[0].scatter(test["LExT [°C]"] - test["SET [°C]"] ,Pow_ratio,label = "experimental points")
    # axs1[0].scatter(test["LExT [°C]"] - test["SET [°C]"] ,Pow_ratio_model, label = "model")
    # axs1[0].set_xlabel("PLR")
    # axs1[0].set_ylabel("COP/COP_fl")
    # axs1[0].set_ylim(0,2)
    # axs1[0].legend()
    
    # axs1[1].scatter(test["PLR"],Pow_ratio,label = "experimental points")
    # axs1[1].scatter(test["PLR"],Pow_ratio_model, label = "model")
    # axs1[1].set_xlabel("PLR")
    # axs1[1].set_ylabel("Pow ratio")
    # axs1[1].set_ylim(0,2)
    # axs1[1].legend()
    
    # plt.tight_layout()
    
    # figure3, axs3 = plt.subplots(1,figsize = (19,9.5))
    # sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
   
    # #Plot
    # x = [0, 0.12, 0.29,0.52, 1]
    # y = [0, 1.02, 1.05, 1.19, 1]
    # axs3.scatter(test["PLR"],COP_ratio,label = "experimental points")
    # axs3.plot(x,y, "red",label = "experimental points")
    # axs3.set_xlabel("PLR")
    # axs3.set_ylabel("COP/COP_fl")
    # axs3.set_ylim(0,3)
    # axs3.legend()
    
    
    
    #Error plot
    figure2, axs2 = plt.subplots(1,2,figsize = (19,9.5))
    sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
    axs2[0].scatter(test["COP"] ,COP_pred,label = "experimental points", c = test["PLR"], cmap='jet')
    axs2[0].set_xlim(0,10)
    axs2[0].set_ylim(0,10)
    axs2[0].plot([0, 10], [0, 10], "k--", label = "Bisector")
    axs2[0].plot([0, 10], [0, 12], "k--", label = "Error +20%")                    
    axs2[0].text( 6, 4.5, "-20%")
    axs2[0].plot([0, 10], [0, 8], "k--", label = "Error -20%")
    axs2[0].text( 6, 7.7, "+20%")
    axs2[0].set_xlabel("COP")
    axs2[0].set_ylabel("COP_pred")
    
    axs2[1].scatter(test["Pow [kW]"] ,Pow_ratio_model * test["Pow full [kW]"],label = "experimental points",c = test["PLR"], cmap='jet')
    axs2[1].set_xlim(0,3)
    axs2[1].set_ylim(0,3)
    axs2[1].plot([0, 10], [0, 10], "k--", label = "Bisector")
    axs2[1].plot([0, 10], [0, 12], "k--", label = "Error +20%")                    
    axs2[1].text( 6, 4.5, "-20%")
    axs2[1].plot([0, 10], [0, 8], "k--", label = "Error -20%")
    axs2[1].text( 6, 7.7, "+20%")
    axs2[1].set_xlabel("Pow")
    axs2[1].set_ylabel("Pow_pred")
    
    #3D plot dependency
    # figure2, axs2 = plt.subplots(subplot_kw={"projection": "3d"})
    # sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
    # # X = - test["PLR"]
    # # Y = test["LExT [°C]"] - test["SET [°C]"]
    # X = - test["PLR"]*(test["LExT [°C]"] - test["SET [°C]"])**2
    # Y = test["PLR"]*test["LExT [°C]"]**2
    # Z = Pow_ratio
    
    # axs2.set_xlabel('X')
    # axs2.set_ylabel('Y')
    # axs2.set_zlim(0,1)
    # axs2.set_zlabel('Pow_ratio')
    

    # # Plot the surface
    # axs2.scatter(X, Y, Z, c = Y, cmap = "jet",
    #                    linewidth=0, antialiased=False)
                       
def cum_value_plot(test):  
    bins = np.arange(0,1.1,0.1)
    y = test["PLR"].value_counts(bins = bins,sort = True)
    y.sort_index(inplace=True) 
    cum_sum = np.zeros(11)
    for i in range(0,len(y)+1):
        cum_sum[i] = sum(y[0:i])
    cum_sum = cum_sum[1:]
    x = np.arange(0.05,1,0.1)
    

    figure3, axs3 = plt.subplots(1,2,figsize = (19,9.5))
    sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
    
    axs3[0].plot(x,cum_sum)
    # plt.plot(line_x,line_y,"k--")
    axs3[0].set_xlabel("PLR")
    # axs3[0].set_xticks(np.arange(min(x), max(x), 0.05))
    axs3[0].set_ylabel("Cum frequency")
    
    br1 = np.arange(len(x)) 
    
    axs3[1].bar(br1,np.array(y),width = 0.5)
    # plt.plot(line_x,line_y,"k--")
    axs3[1].set_xlabel("PLR")
    
    # axs3[1].set_xticks(br1,)
    axs3[1].set_ylabel("Cum frequency")
   
def plot_fl(test):
    
    figure4, axs4 = plt.subplots(1,figsize = (19,9.5))
    sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
    
    filt_test = test.loc[test["PLR"] >= 0.95]
    filt_test = filt_test.loc[filt_test["Status"] == "STATIONARY"]
    LExT_desh = []
    for i in filt_test.index:
        LExT = filt_test.loc[i,"LExT [°C]"]
        if LExT >= 30 and LExT <= 40:
            LExT_desh.append(35)
        elif LExT > 40 and LExT <= 50:
            LExT_desh.append(45)
        elif LExT > 50:
            LExT_desh.append(55)
        else:
            LExT_desh.append(0)
    
    filt_test["LExT_desh"] = LExT_desh
    
    fil1 = filt_test.loc[filt_test["LExT_desh"] == 35]
    fil2 = filt_test.loc[filt_test["LExT_desh"] == 45]
    fil3 = filt_test.loc[filt_test["LExT_desh"] == 55]
    fil4 = filt_test.loc[filt_test["LExT_desh"] == 0]
    
    axs4.scatter(fil1["SET [°C]"],fil1["Pow [kW]"],c = "red", label = "35°C")
    axs4.scatter(fil2["SET [°C]"],fil2["Pow [kW]"],c = "blue", label = "45°C")
    axs4.scatter(fil3["SET [°C]"],fil3["Pow [kW]"],c = "green", label = "55°C")
    axs4.scatter(fil4["SET [°C]"],fil4["Pow [kW]"],c = "grey", label = "off design")
    axs4.scatter(filt_test["SET [°C]"],filt_test["Pow full [kW]"])
    axs4.set_xlabel("SET [°C]")
    axs4.set_ylabel("Pow [kW]")
    axs4.legend()
    print("Tot n points PLR >= 0.95:", len(LExT_desh))
    
def cum_value_LExT_plot(test):
    
    test = test.loc[test["PLR"]>= 0.95]
    
    bins = [0,5, 10,15, 20,25, 30,35, 40,45, 50,55, 60]
    labels = ['0-5', '5-10','10-15','15-20', '20-25','25-30', '30-35','35-40','40-45','45-50','50-55,','55-60']

    # Categorizzare i dati nei bin
    test['range'] = pd.cut(test['LExT [°C]'], bins=bins, labels=labels, right=False)
    counts = test['range'].value_counts().sort_index()
    
    figure3, axs3 = plt.subplots(1,figsize = (19,9.5))
    sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
    
    
    # y = [box_below30, box35, box45, box55, box_above60]
    # x_ticks = ["Below (30)°C","[30,40) °C","[40,50) °C","[50,60) °C", "Above [60]° C"]
    br1 = np.arange(len(labels)) 
    
    axs3.bar(br1,np.array(counts),width = 0.5)
    axs3.set_xlabel("LExT")
    axs3.set_xticks(br1,labels)
    plt.tight_layout()


    
    
    
    
    
#%% Processing test

devices = [
           # "Valliant A+ 5kW  ID5 01-11-2022_28-02-2023",
           # "Valliant A+ 5kW  ID9 01-11-2022_28-02-2023",
           # "Valliant A+ 5kW  ID24 01-11-2022_28-02-2023",
           # "Riello NXHM 10 kW ID458 01-11-2024_28-02-2025",
           "Riello NXHM 10 kW ID526 01-11-2024_28-02-2025",
           # "NIBE 2050 10 kW ID65 01-11-2024_28-02-2025",
           # "NIBE 2050 10 kW ID167 01-11-2024_28-02-2025",
           # "NIBE 2050 10 kW ID531 01-11-2024_28-02-2025",
           # "NIBE F2040 12 kW ID61 01-11-2024_28-02-2025"
           ]
                  
for dev in devices:
    
    test = pd.read_excel(os.path.join('..','Data',f"{dev}.xlsx"), sheet_name = "Test")
    train =  pd.read_excel(os.path.join('..','Data',f"{dev}.xlsx"), sheet_name = "SetData")

    #Filter
    test = test[test['Status'] == 'STATIONARY']
    # test = test[(test['Status'] == 'ACCELERATION') | (test['Status'] == 'DECELERATION')
              # | (test['Status'] == 'STATIONARY')]
    # test = test[test['PLR'] >= 0.3]
    
    LExT_mean = np.mean(test["LExT [°C]"])
    LExT_std = np.std(test["LExT [°C]"])
    LExT_Err = LExT_std/math.sqrt(len(test.index))
    print("Mean Operative Water Temperatue:", LExT_mean,"+-",2 * LExT_std)
    
    test_fl = test.loc[test["PLR"] >= 0.95]
    LExT_mean_fl = np.mean(test_fl["LExT [°C]"])
    LExT_std_fl = np.std(test_fl["LExT [°C]"])
    LExT_Err_fl = LExT_std_fl/math.sqrt(len(test_fl.index))
    print("Mean Operative Water Temperatue fl:", LExT_mean_fl,"+-",2 * LExT_std_fl)
    
    COP_fl_model = test["Heat Cap COND full [kW]"]/ test["Pow full [kW]"]
    COP_ratio = test["COP"]/COP_fl_model
    COP_fl_train =  train["Heat Cap COND full [kW]"]/ train["Pow full [kW]"]
    COP_ratio_train = train["PLR"]/COP_fl_train
    
    train_delta = train["LExT [°C]"]- train["SET [°C]"]
    test_delta = test["LExT [°C]"]- test["SET [°C]"]
    
    Pow_ratio = test["Pow [kW]"]/test["Pow full [kW]"]
    Pow_ratio_train = train["Pow [kW]"]/train["Pow full [kW]"]
    
    corr_dict_COP = {"COP_ratio": COP_ratio,
                 "PLR": test["PLR"],
                 # "PLR^2":test["PLR"]**2,
                 # "PLR^3":test["PLR"]**3, 
                 "LExT": test["LExT [°C]"],
                 "SET": test["SET [°C]"]
                }
    
    
    
    corr_dict_Pow = {"Pow_ratio": Pow_ratio,
                     "PLR": test["PLR"],
                     # "PLR^2":test["PLR"]**2,
                     # "PLR^3":test["PLR"]**3,
                     "LExT": test["LExT [°C]"],
                     "SET": test["SET [°C]"],
                     # "PLR*SET":test["PLR"]*test["SET [°C]"],
                     # "PLR*LExT":test["PLR"]*test["LExT [°C]"],
                     "Delta": test["LExT [°C]"]- test["SET [°C]"],
                     # "ratio": test["LExT [°C]"]/test["SET [°C]"]*test["PLR"],
                     # "exp_lext":np.exp(test["LExT [°C]"]),
                     # "exp_set":np.exp(test["SET [°C]"])
                     }
    
    LExT_test = test["LExT [°C]"]
    SET_test = test["SET [°C]"]
    Delta1_test = LExT_test - SET_test
    PLR_test = test["PLR"]
    
    test_exp = {
            "Pow_ratio":Pow_ratio,
            "COP": test["COP"],
            "SET": test["SET [°C]"],
            "LExT": test["LExT [°C]"],
            "Delta": test["LExT [°C]"]- test["SET [°C]"],
            "PLR": test ["PLR"],
            "SET^2": SET_test**2,
            "Delta^2": (test["LExT [°C]"]- test["SET [°C]"])**2,
            "LExT^2": LExT_test**2,
            "PLR^2": PLR_test**2,
            "SET*LExT": SET_test*LExT_test,
            "SET*Delta": SET_test*Delta1_test,
            "LExT*Delta": LExT_test*Delta1_test,
            "LExT*PLR": test["LExT [°C]"]*test ["PLR"],
            "PLR*Delta": test ["PLR"]*(test["LExT [°C]"]- test["SET [°C]"]),
            "SET*PLR": test["SET [°C]"] * test ["PLR"],
            "SET^3":SET_test**3,
            "SET^2*LExT":(SET_test**2)*LExT_test,
            "SET^2*Delta":(SET_test**2)*Delta1_test,
            "SET^2*PLR": (SET_test**2)*PLR_test,
            "Delta^2*SET": (Delta1_test**2)*SET_test,
            "Delta^3": Delta1_test**3,
            "Delta^2*LExT": (Delta1_test**2)*LExT_test,
            "Delta^2*PLR": ((test["LExT [°C]"]- test["SET [°C]"])**2)*test ["PLR"],
            "LExT^2*SET":(LExT_test**2)*SET_test,
            "LExT^2*Delta":(LExT_test**2)*Delta1_test,
            "LExT^3": LExT_test**3,
            "LExT^2*PLR":(LExT_test**2)*PLR_test,
            "PLR^2*SET": (PLR_test**2)*SET_test,
            "PLR^2*Delta": (PLR_test**2)*Delta1_test,
            "PLR^2*LExT": (PLR_test**2)*LExT_test,
            "PLR^3":PLR_test**3
            }
    #Corr matrix
    corr_df_COP = pd.DataFrame(corr_dict_COP)
    test_pearson_COP = corr_df_COP.corr(method="pearson")
    test_spearman_COP = corr_df_COP.corr(method="spearman")
    
    corr_df_Pow = pd.DataFrame(corr_dict_Pow)
    test_pearson_Pow = corr_df_Pow.corr(method="pearson")
    test_spearman_Pow = corr_df_Pow.corr(method="spearman")
    
    corr_df = pd.DataFrame(corr_dict_Pow)
    test_pearson_Pow = corr_df.corr(method="pearson")
    test_spearman_Pow = corr_df.corr(method="spearman")

#%% Lasso regression + RFE
    # X = corr_df.loc[:,(corr_df.columns != "Pow_ratio") & (corr_df.columns != "COP")]
    # y = corr_df.loc[:,"Pow_ratio"]
    
    # model = LassoCV(cv=5, max_iter=5000).fit(X, y)
    # selected_features = X.columns[model.coef_ != 0]
    # # print(selected_features)
    
    
    # rfe = RFE(model, n_features_to_select= 2)  # Voglio solo 2 feature finali
    # rfe.fit(X, y)

    # #Visualizzo le feature selezionate
    # selected_features = X.columns[rfe.support_]
    # print(selected_features)
        
#%% Create model of regression
    #Split the model in two submodels
    
    # test1 = test.loc[test["PLR"] <= 0.25]
    # test2 = test.loc[test["PLR"] > 0.25]
    
    # train1 = train.loc[train["PLR"] <= 0.25]
    # train2 = train.loc[train["PLR"] > 0.25]
    
    # X_train = np.column_stack((train["PLR"],train["LExT [°C]"]-train["SET [°C]"]))
    # X_test = np.column_stack((test["PLR"],test["LExT [°C]"]-test["SET [°C]"]))
    
    # X_train = np.array(train["PLR"]).reshape(-1, 1)
    # X_test = np.array(test["PLR"]).reshape(-1, 1)
    
    # X_train = np.column_stack(( train["PLR"]/train_delta * train["Pow full [kW]"],(train["PLR"]/train_delta * train["Pow full [kW]"])**2 ))
    # X_test = np.column_stack(( test["PLR"]/test_delta * test["Pow full [kW]"],(test["PLR"]/test_delta * test["Pow full [kW]"])**2))
    
    # X_train = np.column_stack((train["PLR"]*(train["LExT [°C]"]-train["SET [°C]"])**2,train["PLR"]*train["LExT [°C]"]**2))
    # X_test = np.column_stack((test["PLR"]*(test["LExT [°C]"]-test["SET [°C]"])*2,test["PLR"]*test["LExT [°C]"]**2))
    X_train = np.column_stack((train["PLR"],train["PLR"]/(train["LExT [°C]"]-train["SET [°C]"])))
    X_test = np.column_stack((test["PLR"],test["PLR"]/(test["LExT [°C]"]-test["SET [°C]"])))
       
    
    COP_fl_train = train["Heat Cap COND full [kW]"]/train["Pow full [kW]"]
    Y_train_COP = train["COP"]/ COP_fl_train
    Y_train_Pow = train["Pow [kW]"]/train["Pow full [kW]"]
    # Y_train_Pow = train["Pow [kW]"]
    
    # Picewise
    model_reg_Pow = pwlf.PiecewiseLinFit(train["PLR"],Y_train_Pow)
    z = model_reg_Pow.fit_with_breaks([0,0.2,1])
    y = model_reg_Pow.predict(z)    
    Pow_ratio_pred = model_reg_Pow.predict(test["PLR"])
    Pow_ratio_pred_train = model_reg_Pow.predict(train["PLR"])
    
    #Linear Rgression
    # model_reg_Pow = linear_model.LinearRegression(fit_intercept = True).fit(X_train, Y_train_Pow)
    # Pow_ratio_pred = model_reg_Pow.predict(X_test)
    
    #BayesianRidge
    # model_reg_Pow = BayesianRidge()
    # model_reg_Pow.fit(X_train, Y_train_Pow)
    
    #Curve-fit
    # def model_reg_Pow(X, a, b, c, d):
    #     x = X[:,0]
    #     y = X[:,1]
      
    #     return   a* np.log(-x + 1e-6) + b * y**c + d
    
    # scaler_x = StandardScaler()
    # scaler_y = StandardScaler()
    
    # X_scaled = scaler_x.fit_transform(X_train) # shape (2, N)
    # y_scaled = scaler_y.fit_transform(np.array(Y_train_Pow).reshape(-1, 1)).flatten()
    
    
    # params, _ = curve_fit(model_reg_Pow, X_scaled, y_scaled, maxfev = 10000)
    # a, b, c, d = params
    
    # #%%Symbolic regression
    # model = PySRRegressor(
    #     niterations=100,                # più iterazioni → maggiore precisione
    #     population_size=100,            # dimensione della popolazione evolutiva
    #     select_k_features=3,            # (opzionale) quante feature selezionare
    #     model_selection="accuracy",
    #     maxsize = 7,
    #     temp_equation_file=True,        
    #     binary_operators=["+", "-", "*", "/"],
    #     loss="loss(x, y) = (x - y)^2",  # funzione di loss personalizzabile
    # )
    
    # X_test = np.column_stack((test["PLR"],test["LExT [°C]"],test["SET [°C]"]))
    # y = np.array(Pow_ratio)
    # model.fit(X_test, y)
    # print(model.get_best())

    # # print(f"Pow_ratio ≈ {a:.3f}·PLR + {b:.3f}·PLR² + {c:.3f}·log(DeltaT) + {d:.3f}")
    # Pow_ratio_pred_scaled = model_reg_Pow(X_test,*params)
    # Pow_ratio_pred = scaler_y.inverse_transform(Pow_ratio_pred_scaled.reshape(-1, 1)).flatten()
    
    # # Pow_ratio_pred = model_reg_Pow.predict(X_test)
    # Pow_pred =  Pow_ratio_pred * test["Pow full [kW]"]
    # COP_pred = test["Heat Cap COND [kW]"]/Pow_pred
    
    # Pow_ratio_pred_train = model_reg_Pow.predict(X_train)
    # Pow_pred_train =  Pow_ratio_pred_train* train["Pow full [kW]"]
    # COP_pred_train = train["Heat Cap COND [kW]"]/Pow_pred_train
    
    print("PowR_model_score:",r2_score(Pow_ratio, Pow_ratio_pred))
    # print("Pow_model_score:",r2_score(Pow_pred, test["Pow [kW]"]))
    # print("COP_model_RMSE:",root_mean_squared_error(COP_ratio, COP_ratio_pred))
    print("PowR_model_RMSE:",root_mean_squared_error(Pow_ratio, Pow_ratio_pred))
    # print("Pow_model_RMSE:",root_mean_squared_error(Pow_pred, test["Pow [kW]"]))
    # print("COP_model_MAPE:",mean_absolute_percentage_error(COP_ratio, COP_ratio_pred))
    print("PowR_model_MAPE:",mean_absolute_percentage_error(Pow_ratio, Pow_ratio_pred))
    # print("Pow_model_MAPE:",mean_absolute_percentage_error(Pow_pred, test["Pow [kW]"]))
    
    #Perfomance evaluation on catalogue data
    # print("\nPow_model_score:",r2_score(Pow_ratio_train, Pow_ratio_pred_train))
    # print("Pow_model_RMSE:",root_mean_squared_error(Pow_ratio_train, Pow_ratio_pred_train))
    # print("Pow_model_MAPE:",mean_absolute_percentage_error(Pow_ratio_train, Pow_ratio_pred_train))
    
    
    # COP_Pow_PLR_plot(test,Pow_ratio_pred)
    # cum_value_plot(test)    
    plot_fl(test)
    # cum_value_LExT_plot(test)


    # figure5, axs5 = plt.subplots(1,2,figsize = (19,9.5))
    # sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')

    # axs5[0].hist(test["LExT [°C]"], color='lightgreen', ec='black', bins=15)
    # axs5[1].hist(test["SET [°C]"], color='orange', ec='black', bins=15)














    
    
    