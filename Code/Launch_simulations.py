import pandas as pd
import os
import json
from models import *
from kpi import *

#%% Launch Function------------------------------------------------------------

devices = ['Galletti MLI 18 kW',
           'Galletti MLI 18 kW',
           'Galletti MLI 26 kW',
           'Galletti MLI 30 kW']

def launch(MachineName, source):
    
    "Import Data" 
    df_set = pd.read_excel(os.path.join('..', 'Data', f'{MachineName}.xlsx'), sheet_name="SetData")
    df_test = pd.read_excel(os.path.join('..', 'Data', f'{MachineName}.xlsx'), sheet_name="Test")
    curve = pd.read_excel(os.path.join('..', 'Data',  f'{MachineName}.xlsx'), sheet_name="curve")
     
    Models = load_models(df_set, curve, source)
    KPI = load_test(Models, df_test, curve, f'{MachineName}')
    global Simulation_Results
    Simulation_Results = {"Models": Models, "KPI": KPI}
    # load_graph1(KPI, df_test,  f'{MachineName}')
    # load_graph2(KPI, df_test, f'{MachineName}')
    
    with open(os.path.join('..',"Results",f"{MachineName}",f'{MachineName}_KPI_clust.json'), 'r') as f:
        Res_cluster = json.load(f)

    return Simulation_Results, Res_cluster
#%% Galletti ML1 18kW----------------------------------------------------------

launch('Galletti MLI 18 kW','Water')
f = import_json('Galletti MLI 18 kW')
#%% Galletti ML1 22kW----------------------------------------------------------
   
#launch('Galletti MLI 18 kW','Water')

#%% Galletti ML1 26kW----------------------------------------------------------
   
#launch('Galletti MLI 26 kW','Water')

#%% Galletti ML1 30kW----------------------------------------------------------
   
#launch('Galletti MLI 30 kW','Water')

#%% WPL_A_HK 07 Premium----------------------------------------------------------
   
#launch('WPL_A_HK 07 Premium','Water')
KPI_clust = []

for dev in devices:
    file =  import_json(f"{dev}")
    KPI_clust.append(file)




















































 