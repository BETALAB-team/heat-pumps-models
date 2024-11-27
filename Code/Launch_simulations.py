import pandas as pd
import os
import json
from models import *
from kpi import *

#%% Launch Function------------------------------------------------------------

def launch(MachineName, source):
    
    "Import Data" 
    df_set = pd.read_excel(os.path.join('..', 'Data', f'{MachineName}.xlsx'), sheet_name="SetData")
    df_test = pd.read_excel(os.path.join('..', 'Data', f'{MachineName}.xlsx'), sheet_name="Test")
    curve = pd.read_excel(os.path.join('..', 'Data',  f'{MachineName}.xlsx'), sheet_name="curve")
     
    Models = load_models(df_set, curve, source)
    KPI = load_test(Models, df_test, curve, f'{MachineName}')
    global Simulation_Results
    Simulation_Results = {"Models": Models, "KPI": KPI}
    load_graph(KPI, df_test,  f'{MachineName}')
    
    return Simulation_Results
 
#%% Galletti ML1 18kW----------------------------------------------------------
   
launch('Galletti MLI 18 kW','Water')

#%% Galletti ML1 18kW----------------------------------------------------------
   
launch('Galletti MLI 18 kW','Water')










 