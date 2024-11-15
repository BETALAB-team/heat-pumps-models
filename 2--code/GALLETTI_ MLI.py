import pandas as pd
import os
from models import *
from kpi import *
import numpy as np

#%%----------------------------------------------------------------------------

"Import Data" 
df = pd.read_excel(os.path.join('..', '1--data', 'Galletti MLI 18 kW.xlsx'), sheet_name="SetData")
curve=pd.read_excel(os.path.join('..', '1--data', 'Galletti MLI 18 kW.xlsx'), sheet_name="curve")

Models = load_models(df, curve)
KPI = load_test(df, curve)