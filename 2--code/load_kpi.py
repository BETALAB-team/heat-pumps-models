import pandas as pd
import os
from load_models import *
from kpi import *
"Import Data" 
import numpy as np

df = pd.read_excel(os.path.join('..', '1--data', 'Galletti MLI 18 kW.xlsx'), sheet_name="SetData")
curve=pd.read_excel(os.path.join('..', '1--data', 'Galletti MLI 18 kW.xlsx'), sheet_name="curve")

Models = load_models(df, curve)
Test = {}

#%% Test H01D01----------------------------------------------------------------
    
Test['H01D01'] = kpi_h01d01(Models, df, curve)

#%% Test H01D02----------------------------------------------------------------
    
Test['H01D02'] = kpi_h01d02(Models, df, curve)




