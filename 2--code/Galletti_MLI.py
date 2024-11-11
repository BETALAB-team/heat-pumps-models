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

#%% H10N

Model['H01N - mod A'] = model_h01n(df, curve, indirect_model = "ISO 13612-2 mod A")
Model['H01N - mod B'] = model_h01n(df, curve, indirect_model = "ISO 13612-2 mod B")
Model['H01N - mod C'] = model_h01n(df, curve, indirect_model = "C method")
 

# fig, axs1 = plt.subplots(1,1, figsize = (19,9.5))
# axs1.scatter(Y, Y_pred, edgecolor = 'k', label='COP')
# axs1.set_xlabel('to mare')
# axs1.axline((0, 0), slope=1, color="black", linestyle=(0, (5, 5)))
# axs1.axline((0, 0), slope=0.7, color="black", linestyle=(0, (5, 5)), label = 'CI 30%')
# axs1.axline((0, 0), slope=1.3, color="black", linestyle=(0, (5, 5)), )
# axs1.set_xlim([0, 6.5])
# axs1.set_ylim([0, 6.5])
# axs1.set_title('sono ebete')
# axs1.legend()
# fig.savefig('model_2.png', dpi = 600)


