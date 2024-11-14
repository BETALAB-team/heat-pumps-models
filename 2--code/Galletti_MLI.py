import pandas as pd
import os
from models import *

"Import Data" 
import numpy as np
from sklearn import linear_model

df = pd.read_excel(os.path.join('..', '1--data', 'Galletti MLI 18 kW.xlsx'), sheet_name="SetData")
curve=pd.read_excel(os.path.join('..', '1--data', 'Galletti MLI 18 kW.xlsx'), sheet_name="curve")

Model={}

#%% H01D01---------------------------------------------------------------------

Model['H01D01']  = model_h01d01(df)
 
#%% H01D02---------------------------------------------------------------------

Model['H01D02'] = model_h01d02(df)

#%% H10N-----------------------------------------------------------------------

Model['H01N - mod A'] = model_h01n(df, curve, indirect_model = "ISO 13612-2 mod A")
Model['H01N - mod B'] = model_h01n(df, curve, indirect_model = "ISO 13612-2 mod B")
Model['H01N - mod C'] = model_h01n(df, curve, indirect_model = "C method")
 
#%% H02D01---------------------------------------------------------------------

Model['H02D01'] = model_h02d01(df)

#%% H02D02---------------------------------------------------------------------

Model['H02D02'] = model_h02d02(df)

#%% H02N-----------------------------------------------------------------------

Model['H02N - mod A'] = model_h02n(df, curve, indirect_model = "ISO 13612-2 mod A")
Model['H02N - mod B'] = model_h02n(df, curve, indirect_model = "ISO 13612-2 mod B")  
Model['H02N - mod C'] = model_h02n(df, curve, indirect_model = "C method")
 
#%% H03D01---------------------------------------------------------------------

Model['H03D01'] = model_h03d01(df)

#%% H03D02---------------------------------------------------------------------

Model['H03D02'] = model_h03d02(df)

#%% H03N-----------------------------------------------------------------------

Model['H03N - mod A'] = model_h03n(df, curve, indirect_model = "ISO 13612-2 mod A")
Model['H03N - mod B'] = model_h03n(df, curve, indirect_model = "ISO 13612-2 mod B")  
Model['H03N - mod C'] = model_h03n(df, curve, indirect_model = "C method")

#%% H04D01---------------------------------------------------------------------

Model['H04D01'] = model_h04d01(df)

#%% H04D02---------------------------------------------------------------------

Model['H04D02'] = model_h04d02(df)

#%% H04N-----------------------------------------------------------------------

Model['H04N - mod A'] = model_h04n(df, curve, indirect_model = "ISO 13612-2 mod A")
Model['H04N - mod B'] = model_h04n(df, curve, indirect_model = "ISO 13612-2 mod B")  
Model['H04N - mod C'] = model_h04n(df, curve, indirect_model = "C method")

#%% H05D01---------------------------------------------------------------------

Model['H05D01'] = model_h05d01(df)

#%% H05D02---------------------------------------------------------------------

Model['H05D02'] = model_h05d02(df)

#%% H05N-----------------------------------------------------------------------

Model['H05N - mod A'] = model_h05n(df, curve, indirect_model = "ISO 13612-2 mod A")
Model['H05N - mod B'] = model_h05n(df, curve, indirect_model = "ISO 13612-2 mod B")  
Model['H05N - mod C'] = model_h05n(df, curve, indirect_model = "C method")

#%% H06D01---------------------------------------------------------------------

Model['H06D01'] = model_h06d01(df)

#%% H06D02---------------------------------------------------------------------

Model['H06D02'] = model_h06d02(df)

#%% H05N-----------------------------------------------------------------------

Model['H05N - mod A'] = model_h05n(df, curve, indirect_model = "ISO 13612-2 mod A")
Model['H05N - mod B'] = model_h05n(df, curve, indirect_model = "ISO 13612-2 mod B")  
Model['H05N - mod C'] = model_h05n(df, curve, indirect_model = "C method")



#%% H06N-----------------------------------------------------------------------

Model['H06N - mod A'] = model_h06n(df, curve, indirect_model = "ISO 13612-2 mod A")
Model['H06N - mod B'] = model_h06n(df, curve, indirect_model = "ISO 13612-2 mod B")  
Model['H06N - mod C'] = model_h06n(df, curve, indirect_model = "C method")

#%% H07D01---------------------------------------------------------------------

Model['H07D01'] = model_h07d01(df)

#%% H07D02---------------------------------------------------------------------

Model['H07D02'] = model_h07d02(df)

#%% H07N-----------------------------------------------------------------------

Model['H07N - mod A'] = model_h07n(df, curve, indirect_model = "ISO 13612-2 mod A")
Model['H07N - mod B'] = model_h07n(df, curve, indirect_model = "ISO 13612-2 mod B")  
Model['H07N - mod C'] = model_h07n(df, curve, indirect_model = "C method")

#%% H08D01---------------------------------------------------------------------

Model['H08D01'] = model_h08d01(df)

#%% H08D02---------------------------------------------------------------------

Model['H08D02'] = model_h08d02(df)

#%% H08N-----------------------------------------------------------------------

Model['H08N - mod A'] = model_h08n(df, curve, indirect_model = "ISO 13612-2 mod A")
Model['H08N - mod B'] = model_h08n(df, curve, indirect_model = "ISO 13612-2 mod B")  
Model['H08N - mod C'] = model_h08n(df, curve, indirect_model = "C method")

#%% H09D01---------------------------------------------------------------------

Model['H09D01'] = model_h09d01(df)

#%% H09D02---------------------------------------------------------------------

Model['H09D02'] = model_h09d02(df)

#%% H09N-----------------------------------------------------------------------

Model['H09N - mod A'] = model_h09n(df, curve, indirect_model = "ISO 13612-2 mod A")
Model['H09N - mod B'] = model_h09n(df, curve, indirect_model = "ISO 13612-2 mod B")  
Model['H09N - mod C'] = model_h09n(df, curve, indirect_model = "C method")

#%% H10N-----------------------------------------------------------------------

Model['H10N - mod A'] = model_h10n(df, curve, indirect_model = "ISO 13612-2 mod A")
Model['H10N - mod B'] = model_h10n(df, curve, indirect_model = "ISO 13612-2 mod B")  
Model['H10N - mod C'] = model_h10n(df, curve, indirect_model = "C method")

#%% H11N-----------------------------------------------------------------------

Model['H11N - mod A'] = model_h11n(df, curve, indirect_model = "ISO 13612-2 mod A")
Model['H11N - mod B'] = model_h11n(df, curve, indirect_model = "ISO 13612-2 mod B")  
Model['H11N - mod C'] = model_h11n(df, curve, indirect_model = "C method")

#%% H12N-----------------------------------------------------------------------

Model['H12N - mod A'] = model_h12n(df, curve, indirect_model = "ISO 13612-2 mod A")
Model['H12N - mod B'] = model_h12n(df, curve, indirect_model = "ISO 13612-2 mod B")  
Model['H12N - mod C'] = model_h12n(df, curve, indirect_model = "C method")


































# fig, axs1 = plt.subplots(1,1, figsize = (19,9.5))
# axs1.scatter(Y, Y_pred, edgecolor = 'k', label='COP')
# axs1.set_xlabel('to mare')
# axs1.axline((0, 0), slope=1, color="black", linestyle=(0, (5, 5)))
# axs1.axline((0, 0), slope=0.7, color="black", linestyle=(0, (5, 5)), label = 'CI 30%')
# axs1.axline((0, 0), slope=1.3, color="black", linestyle=(0, (5, 5)), )
# axs1.set_xlim([0, 6.5])
# axs1.set_ylim([0, 6.5])
