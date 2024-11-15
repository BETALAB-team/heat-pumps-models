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
Test = {}

#%% Test H01D01----------------------------------------------------------------
    
Test['H01D01'] = kpi_h01d01(Models, df, curve)

#%% Test H01D02----------------------------------------------------------------
    
Test['H01D02'] = kpi_h01d02(Models, df, curve)

#%% Test H01N------------------------------------------------------------------
    
Test['H01N - mod A'] = kpi_h01n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
Test['H01N - mod B'] = kpi_h01n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
Test['H01N - mod C'] = kpi_h01n(Models, df, curve, indirect_model = "C method")

#%% Test H02D01----------------------------------------------------------------
    
Test['H02D01'] = kpi_h02d01(Models, df, curve)

#%% Test H02D02----------------------------------------------------------------
    
Test['H02D02'] = kpi_h02d02(Models, df, curve)

#%% Test H02N------------------------------------------------------------------
    
Test['H02N - mod A'] = kpi_h02n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
Test['H02N - mod B'] = kpi_h02n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
Test['H02N - mod C'] = kpi_h02n(Models, df, curve, indirect_model = "C method")

#%% Test H03D01----------------------------------------------------------------
    
Test['H03D01'] = kpi_h03d01(Models, df, curve)

#%% Test H03D02----------------------------------------------------------------
    
Test['H03D02'] = kpi_h03d02(Models, df, curve)

#%% Test H03N------------------------------------------------------------------
    
Test['H03N - mod A'] = kpi_h03n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
Test['H03N - mod B'] = kpi_h03n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
Test['H03N - mod C'] = kpi_h03n(Models, df, curve, indirect_model = "C method")

#%% Test H04D01----------------------------------------------------------------
    
Test['H04D01'] = kpi_h04d01(Models, df, curve)

#%% Test H04D02----------------------------------------------------------------
    
Test['H04D02'] = kpi_h04d02(Models, df, curve)

#%% Test H04N------------------------------------------------------------------
    
Test['H04N - mod A'] = kpi_h04n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
Test['H04N - mod B'] = kpi_h04n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
Test['H04N - mod C'] = kpi_h04n(Models, df, curve, indirect_model = "C method")

#%% Test H05D01----------------------------------------------------------------
    
Test['H05D01'] = kpi_h05d01(Models, df, curve)

#%% Test H05D02----------------------------------------------------------------
    
Test['H05D02'] = kpi_h05d02(Models, df, curve)

#%% Test H05N------------------------------------------------------------------
    
Test['H05N - mod A'] = kpi_h05n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
Test['H05N - mod B'] = kpi_h05n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
Test['H05N - mod C'] = kpi_h05n(Models, df, curve, indirect_model = "C method")

#%% Test H06D01----------------------------------------------------------------
    
Test['H06D01'] = kpi_h06d01(Models, df, curve)

#%% Test H06D02----------------------------------------------------------------
    
Test['H06D02'] = kpi_h06d02(Models, df, curve)

#%% Test H06N------------------------------------------------------------------
    
Test['H06N- mod A'] = kpi_h06n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
Test['H06N- mod B'] = kpi_h06n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
Test['H06N- mod C'] = kpi_h06n(Models, df, curve, indirect_model = "C method")

#%% Test H07D01----------------------------------------------------------------
    
Test['H07D01'] = kpi_h07d01(Models, df, curve)

#%% Test H07D02----------------------------------------------------------------
    
Test['H07D02'] = kpi_h07d02(Models, df, curve)

#%% Test H07N------------------------------------------------------------------
    
Test['H07N - mod A'] = kpi_h07n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
Test['H07N - mod B'] = kpi_h07n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
Test['H07N - mod C'] = kpi_h07n(Models, df, curve, indirect_model = "C method")

#%% Test H08D01----------------------------------------------------------------
    
Test['H08D01'] = kpi_h08d01(Models, df, curve)

#%% Test H08D02----------------------------------------------------------------
    
Test['H08D02'] = kpi_h08d02(Models, df, curve)

#%% Test H08N------------------------------------------------------------------
    
Test['H08N - mod A'] = kpi_h08n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
Test['H08N - mod B'] = kpi_h08n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
Test['H08N - mod C'] = kpi_h08n(Models, df, curve, indirect_model = "C method")

#%% Test H09D01----------------------------------------------------------------
    
Test['H09D01'] = kpi_h09d01(Models, df, curve)

#%% Test H09D02----------------------------------------------------------------
    
Test['H09D02'] = kpi_h09d02(Models, df, curve)

#%% Test H09N------------------------------------------------------------------
    
Test['H09N - mod A'] = kpi_h09n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
Test['H09N - mod B'] = kpi_h09n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
Test['H09N - mod C'] = kpi_h09n(Models, df, curve, indirect_model = "C method")


#%% Test H10N------------------------------------------------------------------
    
Test['H10N - mod A'] = kpi_h10n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
Test['H10N - mod B'] = kpi_h10n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
Test['H10N - mod C'] = kpi_h10n(Models, df, curve, indirect_model = "C method")

#%% Test H11N------------------------------------------------------------------
    
Test['H11N - mod A'] = kpi_h11n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
Test['H11N - mod B'] = kpi_h11n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
Test['H11N - mod C'] = kpi_h11n(Models, df, curve, indirect_model = "C method")

#%% Test H12N------------------------------------------------------------------
    
Test['H12N - mod A'] = kpi_h12n(Models, df, curve, indirect_model = "ISO 13612-2 mod A")
Test['H12N - mod B'] = kpi_h12n(Models, df, curve, indirect_model = "ISO 13612-2 mod B")
Test['H12N - mod C'] = kpi_h12n(Models, df, curve, indirect_model = "C method")



























































