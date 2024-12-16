#Read excel
import numpy as np
import os
import pandas as pd
print(os.path.isfile(os.path.join('..',"Data","Selected_device_id_14669.xlsx")))
df = pd.read_excel(os.path.join('..',"Data","Selected_device_id_14669.xlsx")) 
df.replace([np.inf, -np.inf], np.nan, inplace=True) 
df.dropna(inplace=True) 
df = df[df["actual_compressor_speed_heatpump_1"] > 0]
energy = df["power_consumption_compressor_heating_day"] #Wh
energy = list(energy)

for i in range(len(energy)):
    if i == 0:
        energy[i] = energy[i]
    else:
        energy[i] = energy[i] + energy[i-1]

    
df['energy'] = energy
df['time_stamp'] = pd.to_datetime(df['time_stamp'])
hours = df['time_stamp'].dt.hour
minutes = df['time_stamp'].dt.minute

hours = list(hours)
minutes = list(minutes)

for i in range(1,len(hours)):
    hours[i] = hours[i] + minutes[i]/60
    if hours[i] < hours[i-1]:
        hours[i] = hours[i]+hours[i-1]
    else:
        continue
    
power = [0]
d1 = [0]
d2 = [0]


for i in range(1,len(hours)):
    d1.append(energy[i]-energy[i-1])
    d2.append(hours[i]-hours[i-1])
    if d2[i] ==0:
        delta = 0
    else:
        delta = d1[i]/d2[i]*10**-3
    power.append(delta)
    
df['power'] = power #kW    
df['time_stamp'] = hours

file_name = 'Filtered_df_id_14669.xlsx'
filtered_df = df[df["power"] > 1]
filtered_df.to_excel(os.path.join('..',"Data",file_name))

#%% Read excel 2
import numpy as np
import os
import pandas as pd
print(os.path.isfile(os.path.join('..',"Data","logs_winter21.csv")))
df = pd.read_csv(os.path.join('..',"Data","logs_winter21.csv")) 
# df.replace([np.inf, -np.inf], np.nan, inplace=True) 
# df.dropna(inplace=True) 
df = df[df["actual_compressor_speed_heatpump_1"] > 0]
energy = df["power_consumption_compressor_heating_day"] #Wh
energy = list(energy)

for i in range(len(energy)):
    if i == 0:
        energy[i] = energy[i]
    else:
        energy[i] = energy[i] + energy[i-1]

    
df['energy'] = energy
df['time_stamp'] = pd.to_datetime(df['time_stamp'])
hours = df['time_stamp'].dt.hour
minutes = df['time_stamp'].dt.minute

hours = list(hours)
minutes = list(minutes)

for i in range(1,len(hours)):
    hours[i] = hours[i] + minutes[i]/60
    if hours[i] < hours[i-1]:
        hours[i] = hours[i]+hours[i-1]
    else:
        continue
    
power = [0]
d1 = [0]
d2 = [0]


for i in range(1,len(hours)):
    d1.append(energy[i]-energy[i-1])
    d2.append(hours[i]-hours[i-1])
    if d2[i] ==0:
        delta = 0
    else:
        delta = d1[i]/d2[i]*10**-3
    power.append(delta)
    
df['power'] = power #kW    
df['time_stamp'] = hours

file_name = 'Filtered_df_id_14669.xlsx'
filtered_df = df[df["power"] > 1]
filtered_df.to_excel(os.path.join('..',"Data",file_name))
