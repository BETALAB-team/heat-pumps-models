import pandas as pd
import os
from models import *
from kpi import *
import numpy as np
# import seaborn as sns
#import matplotlib.pyplot as plt

#%%----------------------------------------------------------------------------

"Import Data" 
df = pd.read_excel(os.path.join('..', 'Data', 'Galletti MLI 18 kW.xlsx'), sheet_name="SetData")
curve = pd.read_excel(os.path.join('..', 'Data', 'Galletti MLI 18 kW.xlsx'), sheet_name="curve")
 
Models = load_models(df, curve, "Water")
KPI = load_test(Models, df, curve)
load_graph(KPI, df)




















 