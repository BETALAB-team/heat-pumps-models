import numpy as np
from Model_classes import *
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt
#%% Set Seaborn theme
sns.set_theme(rc={'figure.figsize':(19,9.5)},style = 'whitegrid')
    
#%% Devices lists and tests - catalogues
os.chdir('..')

devices = [ #5kW
           ("Valliant A+ 5kW ID9 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           ("Valliant A+ 5kW ID24 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           ("Valliant A+ 5kW ID33 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           ("Valliant A+ 5kW ID77 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           ("Valliant A+ 5kW ID78 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           ("Valliant A+ 5kW ID115 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           ("Valliant A+ 5kW ID151 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           ("Valliant A+ 5kW ID227 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 55-6  A S3 5 kW - DATA","AtW"),
           
           # 10 kW
           # ("Riello NXHM 10 kW ID458 01-09-2024_30-04-2025","Riello NXHM 10 kW - DATA","AtW"),
           # ("Riello NXHM 10 kW ID526 01-09-2024_30-04-2025","Riello NXHM 10 kW - DATA","AtW"),
           # ("NIBE 2050 10 kW ID167 01-09-2024_30-04-2025","NIBE 2050 10 kW - DATA","AtW"),
           # ("NIBE 2050 10 kW ID531 01-09-2024_30-04-2025","NIBE 2050 10 kW - DATA","AtW"),
           # ("NIBE 2050 10 kW ID249 01-09-2024_30-04-2025","NIBE 2050 10 kW - DATA","AtW"),
           
           # 12 kW
           # ("NIBE F2040 12 kW ID61 01-09-2024_30-04-2025","NIBE F2040 12 kW - DATA","AtW"),
           ("Valliant A+ 12kW ID196 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW"),
           ("Valliant A+ 12kW ID208 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW"),
           ("Valliant A+ 12kW ID277 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW"),
           ("Valliant A+ 12kW ID281 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW"),
           ("Valliant A+ 12kW ID305 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW"),
           ("Valliant A+ 12kW ID477 01-09-2024_30-04-2025", "Valliant Aerotherm plus  VWL 125-6  A S3 12 kW - DATA","AtW"),
           
           # #  GeoT
           # ("EcoGEO B1-9 11 kW ID571 01-09-2024_30-04-2025","EcoGEO B1-9 11 kW- DATA","WtW")
           ]

model = [
       
        "A05I01",
        "A05I02",
        "A05I03",
        "A05I05",
        "A05I06",
        "A05I07",
        "A05I08",
        "A05I12",
        
        # "B10I17",
        # "B10I19",
        # "C10I09",
        # "C10I20",
        # "C10I13",
    
        # "D12I04",
        "A12I10",
        "A12I11",
        "A12I14",
        "A12I15",
        "A12I16",
        "A12I18",
        
        # "G11I21",
         ]

#For loop
KPIs = [] 

for dev in devices:
    
    HP = Heat_Pumps(dev)
    HP.status_analysis()
    # HP.plot_test("2025-01-10 00:00:00","2025-01-11 00:00:00",20)
    # HP.plot_test("2025-01-28 00:00:00","2025-01-29 00:00:00",20)
    

    #Modelling
    HP.interp_full_load()
    HP.new_model_fit()
    KPIs.append(HP.KPI)


    #Plots
    # P,S = HP.Selectbest(20)
    # HP.plot_time_series("2025-01-10 00:00:00","2025-01-11 00:00:00",20 )
    # HP.plot_time_series("2025-01-28 00:00:00","2025-01-29 00:00:00",20 )
    
        
KPIs = pd.concat(KPIs)
# KPIs.to_csv(os.path.join('..',"Result Analysis","New models results","KPIs_Def_err.csv"))




        
        
        
