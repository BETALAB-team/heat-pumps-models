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
from gplearn.genetic import SymbolicRegressor
from sympy import *
#%% Methods

#Plot COP ratio as PLR function
def COP_Pow_PLR_plot(test,COP_ratio_model,Pow_ratio_model,COP_pred):
    figure1, axs1 = plt.subplots(1,2,figsize = (19,9.5))
    sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
   
    
    COP_fl_model = test["Heat Cap COND full [kW]"]/ test["Pow full [kW]"]
    COP_ratio = test["COP"]/COP_fl_model
    Pow_ratio = test["Pow [kW]"]/test["Pow full [kW]"]
    
    #Plot
    axs1[0].scatter(test["PLR"] ,COP_ratio,label = "experimental points")
    axs1[0].scatter(test["PLR"] ,COP_ratio_model, label = "model")
    axs1[0].set_xlabel("PLR")
    axs1[0].set_ylabel("COP/COP_fl")
    axs1[0].set_ylim(0,2)
    axs1[0].legend()
    
    axs1[1].scatter(test["PLR"],Pow_ratio,label = "experimental points")
    axs1[1].scatter(test["PLR"],Pow_ratio_model, label = "model")
    axs1[1].set_xlabel("PLR")
    axs1[1].set_ylabel("Pow ratio")
    axs1[1].set_ylim(0,2)
    axs1[1].legend()
    
    plt.tight_layout()
    
    #Error plot
    # figure2, axs2 = plt.subplots(1,2,figsize = (19,9.5))
    # sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
    # axs2[0].scatter(test["COP"] ,COP_pred,label = "experimental points", c = test["PLR"], cmap='jet')
    # axs2[0].set_xlim(0,10)
    # axs2[0].set_ylim(0,10)
    # axs2[0].plot([0, 10], [0, 10], "k--", label = "Bisector")
    # axs2[0].plot([0, 10], [0, 12], "k--", label = "Error +20%")                    
    # axs2[0].text( 6, 4.5, "-20%")
    # axs2[0].plot([0, 10], [0, 8], "k--", label = "Error -20%")
    # axs2[0].text( 6, 7.7, "+20%")
    # axs2[0].set_xlabel("COP")
    # axs2[0].set_ylabel("COP_pred")
    
    # axs2[1].scatter(test["Pow [kW]"] ,Pow_ratio_model * test["Pow full [kW]"],label = "experimental points",c = test["PLR"], cmap='jet')
    # axs2[1].set_xlim(0,3)
    # axs2[1].set_ylim(0,3)
    # axs2[1].plot([0, 10], [0, 10], "k--", label = "Bisector")
    # axs2[1].plot([0, 10], [0, 12], "k--", label = "Error +20%")                    
    # axs2[1].text( 6, 4.5, "-20%")
    # axs2[1].plot([0, 10], [0, 8], "k--", label = "Error -20%")
    # axs2[1].text( 6, 7.7, "+20%")
    # axs2[1].set_xlabel("Pow")
    # axs2[1].set_ylabel("Pow_pred")
    
    #3D plot dependency
    figure2, axs2 = plt.subplots(subplot_kw={"projection": "3d"})
    sns.set_theme(rc={'figure.figsize':(12,9.5)},style = 'whitegrid')
    X = - test["PLR"]
    Y = test["LExT [°C]"] - test["SET [°C]"]
    Z = Pow_ratio
    
    axs2.set_xlabel('PLR')
    axs2.set_ylabel('DeltaT')
    axs2.set_zlim(0,1)
    axs2.set_zlabel('Pow_ratio')
    

    # Plot the surface
    axs2.scatter(X, Y, Z, c = Y, cmap = "jet",
                       linewidth=0, antialiased=False)
                       
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
   
   

#%% Processing test

devices = [
           # "Valliant A+ 5kW  ID5 01-11-2022_28-02-2023",
           # "Valliant A+ 5kW  ID9 01-11-2022_28-02-2023",
           # "Valliant A+ 5kW  ID24 01-11-2022_28-02-2023",
           # "Riello NXHM 10 kW ID458 01-11-2024_28-02-2025",
           # "Riello NXHM 10 kW ID526 01-11-2024_28-02-2025",
           # "NIBE 2050 10 kW ID65 01-11-2024_28-02-2025",
           # "NIBE 2050 10 kW ID167 01-11-2024_28-02-2025",
           # "NIBE 2050 10 kW ID531 01-11-2024_28-02-2025",
           "NIBE F2040 12 kW ID61 01-11-2024_28-02-2025"
           ]
                  
for dev in devices:
    
    test = pd.read_excel(os.path.join('..','Data',f"{dev}.xlsx"), sheet_name = "Test")
    train =  pd.read_excel(os.path.join('..','Data',f"{dev}.xlsx"), sheet_name = "SetData")
    
    #Filter
    test = test[test['Status'] == 'STATIONARY']
    # test = test[(test['Status'] == 'ACCELERATION') | (test['Status'] == 'DECELERATION')
              # | (test['Status'] == 'STATIONARY')]
    # test = test[test['PLR'] >= 0.3]
    
    
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
                     "PLR^2":test["PLR"]**2,
                     "PLR^3":test["PLR"]**3,
                     "LExT": test["LExT [°C]"],
                     "SET": test["SET [°C]"],
                     "PLR*SET":test["PLR"]*test["SET [°C]"],
                     "PLR*LExT":test["PLR"]*test["LExT [°C]"],
                     "Delta": test["LExT [°C]"]- test["SET [°C]"],
                     "ratio": test["LExT [°C]"]/test["SET [°C]"]*test["PLR"],
                     "exp_lext":np.exp(test["LExT [°C]"]),
                     "exp_set":np.exp(test["SET [°C]"])}
    
    LExT_test = test["LExT [°C]"]
    SET_test = test["SET [°C]"]
    Delta1_test = LExT_test - SET_test
    PLR_test = test["PLR"]
    
    test_exp = {
            "Pow":Pow_ratio,
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

 
    
#%% Create model of regression
    #Split the model in two submodels
    
    # test1 = test.loc[test["PLR"] <= 0.25]
    # test2 = test.loc[test["PLR"] > 0.25]
    
    # train1 = train.loc[train["PLR"] <= 0.25]
    # train2 = train.loc[train["PLR"] > 0.25]
    
    # X_train = np.column_stack((train["PLR"],train["PLR"]**2))
    # X_test = np.column_stack((test["PLR"],test["PLR"]**2))
    
    # X_train = np.array(train["PLR"]).reshape(-1, 1)
    # X_test = np.array(test["PLR"]).reshape(-1, 1)
    
    # X_train = np.column_stack(( train["PLR"]/train_delta * train["Pow full [kW]"],(train["PLR"]/train_delta * train["Pow full [kW]"])**2 ))
    # X_test = np.column_stack(( test["PLR"]/test_delta * test["Pow full [kW]"],(test["PLR"]/test_delta * test["Pow full [kW]"])**2))
    
    # X_train = np.column_stack((train["PLR"]*train["LExT [°C]"],train["PLR"]*train["SET [°C]"]))
    # X_test = np.column_stack((test["PLR"]*test["LExT [°C]"],test["PLR"]*test["SET [°C]"]))
    
    X_train = np.column_stack((train["PLR"],train["PLR"]/(train["LExT [°C]"]-train["SET [°C]"])))
    X_test = np.column_stack((test["PLR"],test["PLR"]/(test["LExT [°C]"]-test["SET [°C]"])))
       
    
    COP_fl_train = train["Heat Cap COND full [kW]"]/train["Pow full [kW]"]
    Y_train_COP = train["COP"]/ COP_fl_train
    Y_train_Pow = train["Pow [kW]"]/train["Pow full [kW]"]
    
    #Try picewise linear regression
    # model_reg_COP = pwlf.PiecewiseLinFit(test["PLR"],COP_ratio)
    # z = model_reg_COP.fit_with_breaks([0,0.25,1])
    # y = model_reg_COP.predict(z)
    # COP_ratio_pred = model_reg_COP.predict(test["PLR"])
    
    # #Model regression evaluation
    model_reg_COP = linear_model.LinearRegression(fit_intercept = True).fit(X_train, Y_train_COP)
    COP_ratio_pred = model_reg_COP.predict(X_test)
    
    # model_reg_Pow = pwlf.PiecewiseLinFit(train["PLR"],Y_train_Pow)
    # z = model_reg_Pow.fit_with_breaks([0,0.2,1])
    # y = model_reg_Pow.predict(z)    
    # Pow_ratio_pred = model_reg_Pow.predict(test["PLR"])
    # Pow_ratio_pred_train = model_reg_Pow.predict(train["PLR"])
    
    model_reg_Pow = linear_model.LinearRegression(fit_intercept = True).fit(X_train, Y_train_Pow)
    Pow_ratio_pred = model_reg_Pow.predict(X_test)
    Pow_pred =  Pow_ratio_pred * test["Pow full [kW]"]
    COP_pred = test["Heat Cap COND [kW]"]/Pow_pred
    
    Pow_ratio_pred_train = model_reg_Pow.predict(X_train)
    Pow_pred_train =  Pow_ratio_pred_train* train["Pow full [kW]"]
    COP_pred_train = train["Heat Cap COND [kW]"]/Pow_pred_train
    
    print("Pow_model_score:",r2_score(Pow_ratio, Pow_ratio_pred))
    # print("COP_model_RMSE:",root_mean_squared_error(COP_ratio, COP_ratio_pred))
    print("Pow_model_RMSE:",root_mean_squared_error(Pow_ratio, Pow_ratio_pred))
    # print("COP_model_MAPE:",mean_absolute_percentage_error(COP_ratio, COP_ratio_pred))
    print("Pow_model_MAPE:",mean_absolute_percentage_error(Pow_ratio, Pow_ratio_pred))
    
    #Perfomance evaluation on catalogue data
    print("\n Pow_model_score:",r2_score(Pow_ratio_train, Pow_ratio_pred_train))
    print("Pow_model_RMSE:",root_mean_squared_error(Pow_ratio_train, Pow_ratio_pred_train))
    print("Pow_model_MAPE:",mean_absolute_percentage_error(Pow_ratio_train, Pow_ratio_pred_train))
    
    
    
    COP_Pow_PLR_plot(test,COP_ratio_pred,Pow_ratio_pred,COP_pred)
    # cum_value_plot(test)    
#%%Symbolic regression
    # Create test
    # X =test[["PLR","LExT [°C]","SET [°C]"]]
    # Y = Pow_ratio
    # X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.30)
    
    # #Create model
    # function_set = ['add', 'sub', 'mul', 'div','cos','sin','neg','inv']
    # est_gp = SymbolicRegressor(population_size=5000,function_set=function_set,
    #                        generations=40, stopping_criteria=0.01,
    #                        p_crossover=0.7, p_subtree_mutation=0.1,
    #                        p_hoist_mutation=0.05, 
    #                        p_point_mutation=0.1,
    #                        max_samples=0.9, verbose=1,
    #                        parsimony_coefficient=0.01, random_state=0,
    #                       feature_names=X_train.columns)
    
    # converter = {
    #            'sub': lambda x, y : x - y,
    #            'div': lambda x, y : x/y,
    #            'mul': lambda x, y : x*y,
    #            'add': lambda x, y : x + y,
    #            'neg': lambda x    : -x,
    #            'pow': lambda x, y : x**y,
    #            'sin': lambda x    : sin(x),
    #            'cos': lambda x    : cos(x),
    #            'inv': lambda x: 1/x,
    #            'sqrt': lambda x: x**0.5,
    #            'pow3': lambda x: x**3
    #            } 


    # est_gp.fit(X_train, y_train)
    # print('R2:',est_gp.score(X_test,y_test))
    # next_e = sympify((est_gp._program), locals=converter)
    # next_e

















    
    
    