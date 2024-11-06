import pandas as pd
import os
import numpy as np

from models import model_h01d01, model_h01d02
df = pd.read_excel(os.path.join('..', '1--data', 'Galletti MLI 18 kW.xlsx'), sheet_name="SetData")
L = model_h01d02(df)
#Y_predict, Y, MSE, RMSE,A = model_h01d02(df)
#A=np.array([[1,1,1],[1,1,1]])
#B=np.transpose(A)
#C=np.matmul(A,B)
