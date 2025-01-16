#Read excel
import numpy as np
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

print(os.path.isfile(os.path.join('..',"Data","Selected_device_id_14669.xlsx")))
df = pd.read_excel(os.path.join('..',"Data","Selected_device_id_14669.xlsx")) 
df.replace([np.inf, -np.inf], np.nan, inplace=True) 
df.dropna(inplace=True) 
df = df[df["actual_compressor_speed_heatpump_1"] > 0]
energy = df["power_consumption_compressor_heating_day"] #Wh
energy = list(energy)
deltaE = [0]

for i in range(len(energy)):
    if i == 0:
        deltaE[i] = 0
    # elif energy[i] - energy[i-1]< 0:
    #     deltaE.append(energy[i])
    else:
        deltaE.append(energy[i] - energy[i-1])
 
    
df['energy'] = energy
df['time_stamp'] = pd.to_datetime(df['time_stamp'])
days = df['time_stamp'].dt.day
hours = df['time_stamp'].dt.hour
minutes = df['time_stamp'].dt.minute

days = list(days)
hours = list(hours)
minutes = list(minutes)

for i in range(1,len(hours)):
    hours[i] = days[i] *24 + hours[i] + minutes[i]/60
    # if hours[i] < hours[i-1]:
    #     hours[i] = hours[i]+hours[i-1]
    # else:
    #     continue
    
power = [0]
#d1 = [0]
d2 = [0]


for i in range(1,len(hours)):
    #d1.append(energy[i]-energy[i-1])
    d2.append(hours[i]-hours[i-1])
    if d2[i] == 0:
        delta = 0
    else:
        delta = deltaE[i]/d2[i]*10**-3
    power.append(delta)
    
HC = 4.186* (df["actual_flowtemp"]-df["actual_returntemp"]) * df["hp_water_flow_rate"]/60


# df['deltaT'] = d2 #h
# df['deltaE'] = d1 #Wh
df['power'] = power #kW    
df['time_stamp'] = hours
df['HC'] = HC 
COP = (4.186* (df["actual_flowtemp"]-df["actual_returntemp"]) * df["hp_water_flow_rate"]/60)/ df['power']
df['COP'] = COP 

file_name = 'Filtered_df_id_14669.xlsx'
filtered_df = df[df["power"] > 1 ]
#filtered_df = filtered_df[filtered_df["outside_temperature_27"] > 0]
filtered_df.to_excel(os.path.join('..',"Data",file_name))

figure1, axs1 = plt.subplots(1,figsize = (19,9.5))
figure1.suptitle('Power vs frequency',fontsize = 15)
axs1.scatter(filtered_df["actual_compressor_speed_heatpump_1"],filtered_df["power"] )

figure1, axs1 = plt.subplots(1,figsize = (19,9.5))
figure1.suptitle(' COP vs Text',fontsize = 15)
axs1.scatter(filtered_df["outside_temperature_27"],filtered_df["COP"] )

#%% Read excel 2

import numpy as np
import os
import pandas as pd
print(os.path.isfile(os.path.join('..',"Data","raw_data_NAW006.xlsx")))
df = pd.read_excel(os.path.join('..',"Data","raw_data_NAW006.xlsx"), sheet_name = "tot").astype(float) 
df.replace([np.inf, -np.inf], np.nan, inplace = True) 
df.replace(0,np.nan, inplace = True)
df.dropna(inplace=True) 


file_name = 'Filtered_df_NWA_006.xlsx'
filtered_df = df[df["Pel [kW]"] > 0.5]
filtered_df.to_excel(os.path.join('..',"Data",file_name))































