# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:59:26 2024

@author: vivijac14771
"""


# HeatPumpMonitor.org API example
# Part of the OpenEnergyMonitor project: 
# https://openenergymonitor.org

import requests
import pandas as pd
from tabulate import tabulate
import os
from time import strftime, localtime

#%%

def write_url(system_id, search_keys):
    url = 'https://heatpumpmonitor.org/timeseries/data?id=' + system_id
    myseparator = '&'
    for k,val in list(search_keys.items()):
        new_string = k + '=' + val
        new_url = [url,new_string]
        url = myseparator.join(new_url)
    return url

#%%
system_id = '78'
# Get available data of selected system
url = "https://heatpumpmonitor.org/timeseries/available?id=" + system_id
response = requests.get(url)
available = response.json()

# Download available data of selected system
feeds = available['feeds']
data = pd.DataFrame(columns = list(feeds.keys()))

for feed_key, feed_val in list(feeds.items()):
    
    search_keys = {   'feeds': feed_key, 
                      'start' : '31-08-2024', 
                      'end' : '01-05-2025', 
                      'interval' : '300', #s 
                      'average' : '0', # yes 
                      # 'timeformat' : 'notime'
                      }
    
    url = write_url(system_id, search_keys)

    response = requests.get(url)
    downloaded_data = response.json()
    
    # Save downloaded data 
    data[feed_key] = downloaded_data[feed_key]

#%% Post -processing

time = []
Pow = []
HC = []
LExT = []
LET = []
lfr = []
SET = []

for value in data['heatpump_elec']:
    time.append(value[0]/1000)
    # dt_object = datetime.utcfromtimestamp(inst)
    # time.append(dt_object.strftime('%Y-%m-%d %H:%M:%S'))
    # time.append(strftime('%Y-%m-%d %H:%M:%S', localtime(inst)))
    
for value in data['heatpump_elec']:
    Pow.append(value[1])

for value in data['heatpump_heat']:
    HC.append(value[1])

for value in data['heatpump_flowT']:
    LExT.append(value[1])

for value in data['heatpump_returnT']:
    LET.append(value[1])

# for value in data['heatpump_flowrate']:
    # lfr.append(value[1])

for value in data['heatpump_outsideT']:
    SET.append(value[1])
        
    
post_process_data ={ "Time": time,
                    "heatpump_elec": Pow,
                    "heatpump_heat": HC,
                    "heatpump_flowT": LExT,
                    "heatpump_returnT": LET,
                    # "heatpump_flowrate": lfr,
                    "heatpump_outsideT": SET}  

post_process_data = pd.DataFrame(post_process_data) 
post_process_data['Time'] = pd.to_datetime(post_process_data['Time'], unit = "s")
# post_process_data.index = pd.to_datetime(post_process_data.index)
# start_date = "01-09-2024 00:00:00"
# end_date = "30-04-2025' 00:00:00" 
start_date = "2024-09-01 00:00:00"
end_date = "2025-05-01' 00:00:00" 
filtered_post_process = post_process_data.loc[post_process_data["Time"] >= start_date]
filtered_post_process = filtered_post_process.loc[filtered_post_process["Time"] <= end_date]
filtered_post_process['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')

file_name = "Valliant A+ 5kW ID115 01-09-2024_30-04-2025.xlsx"
filtered_post_process.to_excel(os.path.join("..",'ExpData',file_name))

#%% Compile list of systems with stats
# systems = []
# for system in meta:
#     if str(system['id']) in stats:
#         system['stats'] = stats[str(system['id'])]
#         systems.append(system)

