import os
import pandas as pd 
import numpy as np
from scipy.interpolate import LinearNDInterpolator, RegularGridInterpolator

#Import train and test

def add_index(file):
    print(os.path.isfile(os.path.join(os.getcwd(),f"{file}.xlsx")))
    df = pd.read_excel(os.path.join(os.getcwd(),f"{file}.xlsx"), sheet_name = "Sheet1",).astype(float) 
    # df.dropna(inplace=True) 
    # df.reset_index(drop=True, inplace=True)
    
    n = []
    ONOFF = []
    Trns = []
    
    Pow = df["heatpump_elec"]/1000
    HC = df["heatpump_heat"]/1000
    
    for i in range(len(Pow)):
        if Pow[i] < 0.05 :
            ONOFF.append(0)
        else:
            ONOFF.append(1)
    
    for i in range(len(Pow)):
        if i == 0:
            n.append(0)
        elif abs(Pow[i] - Pow[i-1]) <0.5:
            n.append(0)
        else:
            if Pow[i] < Pow[i-1]:
                n.append(-1)
            elif Pow[i] > Pow[i-1]:
                    n.append(1)
            else:
                n.append(2) #nan values
                
    for i in range(len(Pow)):
        if i == 0:
            Trns.append(0)
        elif ONOFF[i-1] == 0 and ONOFF[i] == 1 and  Pow[i] > Pow[i-1]:
           Trns.append(1)
        elif ONOFF[i-1] == 1 and  ONOFF[i] == 0 and Pow[i] < Pow[i-1]:
           Trns.append(-1)
        else:
            Trns.append(0)
    
    
    df['Index']=pd.Series(n, index= df.index)
    df['Status']=pd.Series(ONOFF)
    df['Turning ON-OFF']=pd.Series(Trns)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df[df['Status'] == 1]
    file_name = f"{file}.xlsx"
    df.to_excel(os.path.join(os.getcwd(),file_name))    
    return df

def interp2D(file):
    train = pd.read_excel(os.path.join(os.getcwd(),f"{file}.xlsx"), sheet_name = "Power").astype(float) 
    test =  pd.read_excel(os.path.join(os.getcwd(),f"{file}.xlsx"), sheet_name = "Sheet1").astype(float)

    #Get Data
    x = np.array(train["SET [°C]"])
    y = np.array(train["LExT [°C]"])
    z = np.array(train["HC [kW]"])
    
    X = np.array(test["SET [°C]"])
    Y= np.array(test["LExT [°C]"])
    LET = np.array(test["LET [°C]"])
    lfr = np.array(test["LFR [kg/s]"])
    Index = np.array(test["Index"])
    HC = np.array(test["heatpump_heat"])/1000
    Pel = np.array(test["heatpump_elec"])/1000
    COP = HC/Pel
    
    # X, Y = np.meshgrid(X,Y)
    
    #Interpolate
    interp = LinearNDInterpolator(list(zip(x, y)), z)
    Z = interp(X,Y)
    PLR = HC/Z
    #Results simulation
    
    res = np.column_stack((X,LET,Y,Pel,Z,HC,lfr,PLR,COP,Index))
    col = ["SET [°C]", "LET [°C]","LExT [°C]","Pel [kW]","HC_full [kW]","HC [kW]", "lfr","PLR","COP","Turning ON-OFF"]
    res = pd.DataFrame(res, columns = col)
    res = res[res['HC_full [kW]'].notna()]
    res = res[res['Pel [kW]'].notna()]
    # res = res[res['Turning ON-OFF'] == -1]
    # res = res[res['PLR'] < 1]
    
    file_name = f"{file}_int.xlsx"
    res.to_excel(os.path.join(os.getcwd(),file_name))
    return res

def interp3D(file):
    train = pd.read_excel(os.path.join(os.getcwd(),f"{file}.xlsx"), sheet_name = "Power").astype(float) 
    test =  pd.read_excel(os.path.join(os.getcwd(),f"{file}.xlsx"), sheet_name = "Sheet1").astype(float)

    #Get Data
    x = np.array(train["SET [°C]"])
    y1 = np.array(train["LExT [°C]"])
    y2 =  np.array(train["LET [°C]"])
    z = np.array(train["HC [kW]"])
    
    X = np.array(test["SET [°C]"])
    Y1= np.array(test["LExT [°C]"])
    Y2 = np.array(test["LET [°C]"])
    lfr = np.array(test["LFR [kg/s]"])
    Index = np.array(test["Index"])
    HC = np.array(test["heatpump_heat"])/1000
    Pel = np.array(test["heatpump_elec"])/1000
    COP = HC/Pel
    
    # X, Y = np.meshgrid(X,Y)
    
    #Interpolate
    interp = LinearNDInterpolator(list(zip(x, y1,y2)), z)
    Z = interp(X,Y1,Y2)
    PLR = HC/Z
    #Results simulation
    
    res = np.column_stack((X,Y2,Y1,Pel,Z,HC,lfr,PLR,COP,Index))
    col = ["SET [°C]", "LET [°C]","LExT [°C]","Pel [kW]","HC_full [kW]","HC [kW]", "lfr","PLR","COP","Turning ON-OFF"]
    res = pd.DataFrame(res, columns = col)
    # res = res[res['HC_full [kW]'].notna()]
    # res = res[res['Pel [kW]'].notna()]
    # res = res[res['Turning ON-OFF'] == -1]
    # res = res[res['PLR'] < 1]
    
    # file_name = f"{file}_int.xlsx"
    # res.to_excel(os.path.join(os.getcwd(),file_name))
    return res

# df = add_index("Valliant  ID9 01-11-2022_28_02-2023 5 min")
res = interp2D("Valliant  ID9 01-11-2022_28_02-2023 5 min")
# res = interp3D("Valliant  ID9 01-11-2022_28_02-2023 5 min")

# fil = res[res["COP"]< 2]
# fil = fil[fil["PLR"]<0.4]