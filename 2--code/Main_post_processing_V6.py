# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 10:52:50 2024

@author: borgnic12709
"""

# Main for the postprocessing of simulation results new infiltration rate

#%% Import
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import PercentFormatter
import numpy as np
import os
import geojson
import seaborn as sns

#%% Plot theme:
# Apply default theme:
sns.set_theme(rc={'figure.figsize':(19,9.5)})
matplotlib.rcParams.update({'font.size': 12})
#%% Classes

#%% Methods
def remove_inf(vector):
    # Remove inf values:
    vector.replace([np.inf, -np.inf], np.nan, inplace=True)
    vector.dropna( how="all", inplace=True)
    return vector

def count_values_in_range(error_ranges, vector):
    # error_ranges = list/tuple with labels of error ranges
    # vector = series of values to count
    
    vector = remove_inf(vector)
    
    values_range = []
    lim_sup = - 0.75
    lim_inf = -1.0
    for i in range(len(error_ranges)):
        # if i == 0:
        #     values_range.append(((vector < lim_sup)).sum())
        #     lim_inf = lim_sup
        #     lim_sup += 0.25
        if i == len(error_ranges)-1:
            values_range.append(((vector >= lim_inf)).sum())
        else:
            values_range.append(((vector >= lim_inf) & (vector < lim_sup)).sum())
            lim_inf = lim_sup
            lim_sup += 0.25
    return values_range

def plot_output_relative_error(out_path_489_mod_geom_manual_age, name_fig, name_input_dataset):
    input_path_489_mod_geom_manual_age = out_path_489_mod_geom_manual_age.replace(r'\results main copy', '')
    input_path_489_mod_geom_manual_age = input_path_489_mod_geom_manual_age + rf'/{name_input_dataset}'

    # Import geojson as DataFrame:
    with open(input_path_489_mod_geom_manual_age) as f:
        input_geojson = geojson.load(f)
    input_path_489_mod_geom_manual_age_df = pd.json_normalize(input_geojson['features'])
    input_path_489_mod_geom_manual_age_df = input_path_489_mod_geom_manual_age_df[~input_path_489_mod_geom_manual_age_df.index.duplicated(keep='first')]
    input_path_489_mod_geom_manual_age_df_simulated = input_path_489_mod_geom_manual_age_df.loc[input_path_489_mod_geom_manual_age_df['properties.Simulate'] == True]
    input_path_489_mod_geom_manual_age_df_simulated = input_path_489_mod_geom_manual_age_df_simulated.set_index(input_path_489_mod_geom_manual_age_df_simulated['properties.Name'])

    # Create DataFrame for output analysis:
    df_output_columns = ['id', 'Envelope class','STDMC simulated', 'STDMC measured 1998', 'STDMC measured 2020',
                         'STDMC measured 2021', 'STDMC measured 2022']
    output_analysis_df = pd.DataFrame(0.0, index = np.arange(len(input_path_489_mod_geom_manual_age_df_simulated)), columns = df_output_columns)
    output_analysis_df['id'] = output_analysis_df['id'].astype(str)
    output_analysis_df['Envelope class'] = output_analysis_df['Envelope class'].astype(str)

    # Open DataFrame of measured stdmc consumption:
    input_database_df = pd.read_excel('DATABASE_98_20_21_22.xlsx', index_col = 'ID_UNIVOCO')
    input_database_df = input_database_df.fillna(value = 0)
    input_database_df = input_database_df[~input_database_df.index.duplicated(keep='first')]


    # Open csv file of results:
    i = 0
    for name in input_path_489_mod_geom_manual_age_df_simulated['properties.Name']:
        path_output_building = os.path.join(out_path_489_mod_geom_manual_age,f"Results Bd {name}.csv")
        output_bd_df = pd.read_csv(path_output_building, delimiter = ';', skiprows = [1])

        # Save results into output analysis df (from input df):
        output_analysis_df.loc[i,'id'] = name
        output_analysis_df.loc[i,'Envelope class'] = input_path_489_mod_geom_manual_age_df_simulated.loc[name, 'properties.Envelope']
        output_analysis_df.loc[i,'STDMC simulated'] = output_bd_df['Heating system gas consumption [Nm3]'].sum() / 1.0549
        # Save results into output analysis df (from csv with measured consumption):
        if name in input_database_df.index.values:
            output_analysis_df.loc[i,'STDMC measured 1998'] = input_database_df.loc[name, 'Volume anno 1998']
            output_analysis_df.loc[i,'STDMC measured 2020'] = input_database_df.loc[name, 'Volume anno 2020']
            output_analysis_df.loc[i,'STDMC measured 2021'] = input_database_df.loc[name, 'Volume anno 2021']
            output_analysis_df.loc[i,'STDMC measured 2022'] = input_database_df.loc[name, 'Volume anno 2022']
        
        i += 1

    # Add relative error:
    output_analysis_df['relative_error_1998'] = -1*(output_analysis_df['STDMC measured 1998'] - output_analysis_df['STDMC simulated'])/output_analysis_df['STDMC measured 1998']
    output_analysis_df['relative_error_2020'] = -1*(output_analysis_df['STDMC measured 2020'] - output_analysis_df['STDMC simulated'])/output_analysis_df['STDMC measured 2020']
    output_analysis_df['relative_error_2021'] = -1*(output_analysis_df['STDMC measured 2021'] - output_analysis_df['STDMC simulated'])/output_analysis_df['STDMC measured 2021']
    output_analysis_df['relative_error_2022'] = -1*(output_analysis_df['STDMC measured 2022'] - output_analysis_df['STDMC simulated'])/output_analysis_df['STDMC measured 2022']

    # return output_analysis_df

    # Plot histogram absolute values
    fig1, axs1 = plt.subplots(2, figsize = (19,9.5))
    # count_values_in_range
    # error_ranges = ("< -1.0", '-1.0', "-0.75", "-0.5", '-0.25', '0', '0.25', '0.5', '0.75', '1.0', '> 1.0')
    error_ranges = ('[-1.0 ; -0.75[', "[-0.75 ; -0.5[", "[-0.5 ; -0.25[", '[-0.25 ; 0[', '[0 ; 0.25[', '[0.25 ; 0.5[', '[0.5 ; 0.75[', '[0.75 ; 1.0[', '[1.0 ; 1.25[', '[1.25 ; 1.5[', '[1.5 ; +inf[')
    
    error_values = {
        '2020': count_values_in_range(error_ranges, output_analysis_df['relative_error_2020']),
        '2021': count_values_in_range(error_ranges, output_analysis_df['relative_error_2021']),
        '2022': count_values_in_range(error_ranges, output_analysis_df['relative_error_2022']),
    }

    x = np.arange(len(error_ranges))  # the label locations
    width = 0.2  # the width of the bars
    multiplier = 0

    for attribute, measurement in error_values.items():
        offset = width * multiplier
        rects = axs1[0].bar(x + offset, measurement, width, label=attribute)
        axs1[0].bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    axs1[0].set_xlabel('Relative error range')
    axs1[0].set_ylabel('N buildings')
    axs1[0].set_title(f'Relative error {name_fig}')
    axs1[0].set_xticks(x + width, error_ranges)
    axs1[0].legend()

    # Percentage values:
    vector_1998 = remove_inf(output_analysis_df['relative_error_1998'])
    vector_2020 = remove_inf(output_analysis_df['relative_error_2020'])
    vector_2021 = remove_inf(output_analysis_df['relative_error_2021'])
    vector_2022 = remove_inf(output_analysis_df['relative_error_2022'])
    
    # Check distribution of age classes:
    age_class_distribution = output_analysis_df['Envelope class'].value_counts(normalize = True)
    
    
    # Relative error on total STDMC + age classes distribution:
    total_rel_error_dict = {}
    total_rel_error_dict['rel_err_1998'] = ((-sum(output_analysis_df['STDMC measured 1998']) + sum(output_analysis_df[(output_analysis_df['STDMC measured 1998'] != 0)]['STDMC simulated'])) /
                                            sum(output_analysis_df[(output_analysis_df['STDMC measured 1998'] != 0)]['STDMC measured 1998'])) * 100
    total_rel_error_dict['rel_err_2020'] = ((-sum(output_analysis_df['STDMC measured 2020']) + sum(output_analysis_df[(output_analysis_df['STDMC measured 2020'] != 0)]['STDMC simulated'])) /
                                            sum(output_analysis_df[(output_analysis_df['STDMC measured 2020'] != 0)]['STDMC measured 2020'])) * 100
    total_rel_error_dict['rel_err_2021'] = ((-sum(output_analysis_df['STDMC measured 2021']) + sum(output_analysis_df[(output_analysis_df['STDMC measured 2021'] != 0)]['STDMC simulated'])) /
                                            sum(output_analysis_df[(output_analysis_df['STDMC measured 2021'] != 0)]['STDMC measured 2021'])) * 100
    total_rel_error_dict['rel_err_2022'] = ((-sum(output_analysis_df['STDMC measured 2022']) + sum(output_analysis_df[(output_analysis_df['STDMC measured 2022'] != 0)]['STDMC simulated'])) /
                                            sum(output_analysis_df[(output_analysis_df['STDMC measured 2022'] != 0)]['STDMC measured 2022'])) * 100
    total_rel_error_dict['age_class_distribution'] = age_class_distribution
    total_rel_error_dict['output_analysis_df'] = output_analysis_df
    
    error_values_percentage = {
        '2020': [round((x *100 / len(vector_2020)),1) for x in count_values_in_range(error_ranges, output_analysis_df['relative_error_2020'])],
        '2021': [round((x *100 / len(vector_2021)),1) for x in count_values_in_range(error_ranges, output_analysis_df['relative_error_2021'])],
        '2022': [round((x *100 / len(vector_2022)),1) for x in count_values_in_range(error_ranges, output_analysis_df['relative_error_2022'])],
    }

    x = np.arange(len(error_ranges))  # the label locations
    width = 0.2  # the width of the bars
    multiplier = 0
    
    for attribute, measurement in error_values_percentage.items():
        offset = width * multiplier
        rects = axs1[1].bar(x + offset, measurement, width, label=attribute)
        axs1[1].bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    axs1[1].set_xlabel('Relative error range')
    axs1[1].set_ylabel('% buildings')
    axs1[1].set_title(f'Relative error {name_fig}')
    axs1[1].set_ylim([0, 35])
    axs1[1].set_xticks(x + width, error_ranges)
    axs1[1].legend()

    fig1.tight_layout()
    fig1.savefig(f'{name_fig}_rel_error.jpg', dpi = 400)
    
    return total_rel_error_dict

def age_class_distribution(ED_489_orig_geom_rnd_age_district, distribution_type):
    # Select the typology of distribution for counting values:
    # 1: Eureca new distribution, simulazioni Nicola
    # 2: Eureca old distribution, simulazioni gianmarco
    if distribution_type == 0:
        age_class_eureca = ['< 1930', '1930-1945', '1946-1960', '1961-1976', '1977-1991', '1992-2005', '>2005']
    elif distribution_type == 1:
        age_class_eureca = ['<45', '45-76', '76-91', '91-05', '>2005']
    else: 
        return
    
    distr_489_orig_geom = {}
    for age_class in age_class_eureca:
        if age_class in ED_489_orig_geom_rnd_age_district['age_class_distribution']:
            distr_489_orig_geom[age_class] = ED_489_orig_geom_rnd_age_district['age_class_distribution'].loc[age_class]
        else:
            distr_489_orig_geom[age_class] = 0
    
    # Uniformation if distribution_type == 1:
    if distribution_type == 1:
        distr_489_orig_geom_mod = {}
        distr_489_orig_geom_mod['< 1930'] = distr_489_orig_geom['<45']
        distr_489_orig_geom_mod['1930-1945'] = 0
        distr_489_orig_geom_mod['1946-1960'] = distr_489_orig_geom['45-76'] / 2
        distr_489_orig_geom_mod['1961-1976'] = distr_489_orig_geom['45-76'] / 2
        distr_489_orig_geom_mod['1977-1991'] = distr_489_orig_geom['76-91'] / 2
        distr_489_orig_geom_mod['1992-2005'] = distr_489_orig_geom['91-05'] 
        distr_489_orig_geom_mod['>2005'] = distr_489_orig_geom['>2005']
        return distr_489_orig_geom_mod
    else:
        return distr_489_orig_geom

#%% Main
# Directories' paths of output files:
project_directory_path = r'C:\Users\borgnic12709\OneDrive - Università degli Studi di Padova\Università\21 ANACI\DaBano'

# Put here list of output paths:
out_path_489_mod_geom_manual_age = project_directory_path + r'\12.1 EURECA SIMULATION 489 BLD MOD GEOM MANUAL AGE LOW INFILTRATION\results main copy'
out_path_489_orig_geom_manual_age = project_directory_path + r'\4.1 EURECA SIMULATION 489 BLD ORIGINAL GEOM MANUAL AGE LOW INFILTRATION\results main copy'
out_path_489_mod_geom_fixed_age = project_directory_path + r'\13.1 EURECA SIMULATION 489 BLD MOD GEOM FIXED AGE LOW INFILTRATION\results main copy'
out_path_489_orig_geom_fixed_age = project_directory_path + r'\14.1 EURECA SIMULATION 489 BLD ORIG GEOM FIXED AGE LOW INFILTRATION\results main copy'
out_path_2059_orig_geom_fixed_age = project_directory_path + r'\8.1 EURECA SIMULATION 2059 BLD ORIG GEOM FIXED AGE LOW INFILTRATION\results main copy'
out_path_489_mod_geom_rnd_age_city = project_directory_path + r'\11.1 EURECA SIMULATION 489 BLD MOD GEOM RANDOM AGE CITY LOW INFILTRATION\results main copy'
out_path_489_orig_geom_rnd_age_city = project_directory_path + r'\5.1 EURECA SIMULATION 489 BLD ORIGINAL GEOM RANDOM AGE CITY LOW INFILTRATION\results main copy'
out_path_2059_orig_geom_rnd_age_city = project_directory_path + r'\9.1 EURECA SIMULATION 2059 BLD ORIG GEOM RANDOM AGE CITY LOW INFILTRATION\results main copy'
out_path_489_mod_geom_rnd_age_district = project_directory_path + r'\7.1 EURECA SIMULATION 489 BLD MOD GEOM RANDOM AGE DISTRICT LOW INFILTRATION\results main copy'
out_path_489_orig_geom_rnd_age_district = project_directory_path + r'\6.1 EURECA SIMULATION 489 BLD ORIG GEOM RANDOM AGE DISTRICT LOW INFILTRATION\results main copy'
out_path_2059_orig_geom_rnd_age_district = project_directory_path + r'\10.1 EURECA SIMULATION 2059 BLD ORIG GEOM RANDOM AGE DISTRICT LOW INFILTRATION\results main copy'

#%%
ED_489_mod_geom_manual_age = plot_output_relative_error(out_path_489_mod_geom_manual_age, '489_mod_geom_manual_age', '12.1 dataset_489_bld_mod_geom_manual_age_geom_rip.geojson')
ED_489_orig_geom_manual_age = plot_output_relative_error(out_path_489_orig_geom_manual_age, '489_orig_geom_manual_age', 'dataset_489_original_geom_rip.geojson')
ED_489_mod_geom_fixed_age = plot_output_relative_error(out_path_489_mod_geom_fixed_age, '489_mod_geom_fixed_age', '13.1 dataset_489_bld_mod_geom_fixed_age_geom_rip.geojson')
ED_489_orig_geom_fixed_age = plot_output_relative_error(out_path_489_orig_geom_fixed_age, '489_orig_geom_fixed_age', '14 dataset_489_bld_orig_geom_fixed_age.geojson')
ED_2059_orig_geom_fixed_age = plot_output_relative_error(out_path_2059_orig_geom_fixed_age, '2059_orig_geom_fixed_age', '8.1 dataset_2059_bld_orig_geom_fixed_age_geom_rip.geojson')
ED_489_mod_geom_rnd_age_city = plot_output_relative_error(out_path_489_mod_geom_rnd_age_city, '489_mod_geom_rnd_age_city', '11.1 dataset_489_bld_mod_geom_random_age_city_geom_rip.geojson')
ED_489_orig_geom_rnd_age_city = plot_output_relative_error(out_path_489_orig_geom_rnd_age_city, '489_orig_geom_rnd_age_city', 'dataset_489_orig_geom_rip_random_age_city.geojson')
ED_2059_orig_geom_rnd_age_city = plot_output_relative_error(out_path_2059_orig_geom_rnd_age_city, '2059_orig_geom_rnd_age_city', '9.1 dataset_2059_bld_orig_geom_random_age_city_geom_rip.geojson')
ED_489_mod_geom_rnd_age_district = plot_output_relative_error(out_path_489_mod_geom_rnd_age_district, '489_mod_geom_rnd_age_district', '7 dataset_489_bld_mod_geom_random_age_district_v5_ML.geojson')
ED_489_orig_geom_rnd_age_district = plot_output_relative_error(out_path_489_orig_geom_rnd_age_district, '489_orig_geom_rnd_age_district', '6 dataset_489_bld_orig_geom_random_age_district_v5_ML.geojson')
ED_2059_orig_geom_rnd_age_district = plot_output_relative_error(out_path_2059_orig_geom_rnd_age_district, '2059_orig_geom_rnd_age_district', '10 dataset_2059_bld_orig_geom_random_age_district_v5_ML.geojson')

#%% Plot Errors on whole analyzed district:
fig1, axs1 = plt.subplots(2, figsize = (19,9.5))
# Creation of dict for plotting:
error_ranges = ("489_MGMA", "489_OGMA", "489_MGFA", '489_OGFA', '2059_OGFA', '489_MGRA', '489_OGRA', '2059_OGRA', '489_MGRAD', '489_OGRAD', '2059_OGRAD')
error_values = {
    '1998': [round(ED_489_mod_geom_manual_age['rel_err_1998'],1),
             round(ED_489_orig_geom_manual_age['rel_err_1998'],1),
             round(ED_489_mod_geom_fixed_age['rel_err_1998'],1),
             round(ED_489_orig_geom_fixed_age['rel_err_1998'],1),
             round(ED_2059_orig_geom_fixed_age['rel_err_1998'],1),
             round(ED_489_mod_geom_rnd_age_city['rel_err_1998'],1),
             round(ED_489_orig_geom_rnd_age_city['rel_err_1998'],1),
             round(ED_2059_orig_geom_rnd_age_city['rel_err_1998'],1),
             round(ED_489_mod_geom_rnd_age_district['rel_err_1998'],1),
             round(ED_489_orig_geom_rnd_age_district['rel_err_1998'],1),
             round(ED_2059_orig_geom_rnd_age_district['rel_err_1998'],1),
             ],
    '2020': [round(ED_489_mod_geom_manual_age['rel_err_2020'],1),
             round(ED_489_orig_geom_manual_age['rel_err_2020'],1),
             round(ED_489_mod_geom_fixed_age['rel_err_2020'],1),
             round(ED_489_orig_geom_fixed_age['rel_err_2020'],1),
             round(ED_2059_orig_geom_fixed_age['rel_err_2020'],1),
             round(ED_489_mod_geom_rnd_age_city['rel_err_2020'],1),
             round(ED_489_orig_geom_rnd_age_city['rel_err_2020'],2),
             round(ED_2059_orig_geom_rnd_age_city['rel_err_2020'],1),
             round(ED_489_mod_geom_rnd_age_district['rel_err_2020'],1),
             round(ED_489_orig_geom_rnd_age_district['rel_err_2020'],1),
             round(ED_2059_orig_geom_rnd_age_district['rel_err_2020'],1),
             ],
    '2021': [round(ED_489_mod_geom_manual_age['rel_err_2021'],1),
             round(ED_489_orig_geom_manual_age['rel_err_2021'],1),
             round(ED_489_mod_geom_fixed_age['rel_err_2021'],1),
             round(ED_489_orig_geom_fixed_age['rel_err_2021'],1),
             round(ED_2059_orig_geom_fixed_age['rel_err_2021'],1),
             round(ED_489_mod_geom_rnd_age_city['rel_err_2021'],1),
             round(ED_489_orig_geom_rnd_age_city['rel_err_2021'],1),
             round(ED_2059_orig_geom_rnd_age_city['rel_err_2021'],1),
             round(ED_489_mod_geom_rnd_age_district['rel_err_2021'],1),
             round(ED_489_orig_geom_rnd_age_district['rel_err_2021'],1),
             round(ED_2059_orig_geom_rnd_age_district['rel_err_2021'],1),
             ],
    '2022': [round(ED_489_mod_geom_manual_age['rel_err_2022'],1),
             round(ED_489_orig_geom_manual_age['rel_err_2022'],1),
             round(ED_489_mod_geom_fixed_age['rel_err_2022'],1),
             round(ED_489_orig_geom_fixed_age['rel_err_2022'],1),
             round(ED_2059_orig_geom_fixed_age['rel_err_2022'],1),
             round(ED_489_mod_geom_rnd_age_city['rel_err_2022'],1),
             round(ED_489_orig_geom_rnd_age_city['rel_err_2022'],1),
             round(ED_2059_orig_geom_rnd_age_city['rel_err_2022'],1),
             round(ED_489_mod_geom_rnd_age_district['rel_err_2022'],1),
             round(ED_489_orig_geom_rnd_age_district['rel_err_2022'],1),
             round(ED_2059_orig_geom_rnd_age_district['rel_err_2022'],1),
             ],
}
    
x = np.arange(len(error_ranges))  # the label locations
width = 0.20  # the width of the bars
multiplier = -0.5

for attribute, measurement in error_values.items():
    offset = width * multiplier
    rects = axs1[0].bar(x + offset, measurement, width, label=attribute)
    axs1[0].bar_label(rects, padding=3, rotation = 'vertical')
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
axs1[0].set_xlabel('Relative error range')
axs1[0].set_ylabel('N buildings')
axs1[0].set_title('Relative error total')
axs1[0].set_xticks(x + width, error_ranges)
axs1[0].set_ylim([-25,100])
axs1[0].legend()

fig1.tight_layout()
fig1.savefig('total_rel_error.jpg',dpi = 400)

#%% Plot 2500 (2059) bld different ages assignment comparison:
fig1, axs1 = plt.subplots(1,2, figsize = (19,9.5))

error_ranges = ('Età fissa', 'Età random', 'Età PRG')
error_values = {
    '2020': [round(ED_2059_orig_geom_fixed_age['rel_err_2020'],1),
             round(ED_2059_orig_geom_rnd_age_city['rel_err_2020'],1),
             round(ED_2059_orig_geom_rnd_age_district['rel_err_2020'],1),
             ],
    '2021': [round(ED_2059_orig_geom_fixed_age['rel_err_2021'],1),
             round(ED_2059_orig_geom_rnd_age_city['rel_err_2021'],1),
             round(ED_2059_orig_geom_rnd_age_district['rel_err_2021'],1),
             ],
    '2022': [round(ED_2059_orig_geom_fixed_age['rel_err_2022'],1),
             round(ED_2059_orig_geom_rnd_age_city['rel_err_2022'],1),
             round(ED_2059_orig_geom_rnd_age_district['rel_err_2022'],1),
             ],
}
    
x = np.arange(len(error_ranges))  # the label locations
width = 0.20  # the width of the bars
multiplier = 0

for attribute, measurement in error_values.items():
    offset = width * multiplier
    rects = axs1[0].bar(x + offset, measurement, width, label=attribute)
    axs1[0].bar_label(rects, padding=3, fontsize = 20, rotation = 90)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
axs1[0].set_xlabel('Criterio di assegnazione classe età', fontsize = 18)
axs1[0].set_ylabel('Errore relativo %', fontsize = 20)
# axs1[0].set_title('Relative error for 2548 buildings with different age class assignment criteria')
axs1[0].set_xticks(x + width, error_ranges, fontsize = 18)
axs1[0].set_ylim([0, 100])
axs1[0].legend(fontsize = 20)

# Plot 489 buildings, same age before and after manual geometry correction:
# Creation of dict for plotting:
error_ranges = ('Geometria modificata', 'Geometria originale')
error_values = {
    '2020': [round(ED_489_mod_geom_manual_age['rel_err_2020'],1),
             round(ED_489_orig_geom_manual_age['rel_err_2020'],1),
             ],
    '2021': [round(ED_489_mod_geom_manual_age['rel_err_2021'],1),
             round(ED_489_orig_geom_manual_age['rel_err_2021'],1),
             ],
    '2022': [round(ED_489_mod_geom_manual_age['rel_err_2022'],1),
             round(ED_489_orig_geom_manual_age['rel_err_2022'],1),
             ],
}
    
x = np.arange(len(error_ranges))  # the label locations
width = 0.20  # the width of the bars
multiplier = 0

for attribute, measurement in error_values.items():
    offset = width * multiplier
    rects = axs1[1].bar(x + offset, measurement, width, label=attribute)
    axs1[1].bar_label(rects, padding=3, fontsize = 20)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
axs1[1].set_xlabel('Tipo di geometria', fontsize = 18)
axs1[1].set_ylabel('Errore relativo %', fontsize = 18)
# axs1[1].set_title('Relative error for 489 buildings before and after geometry correction')
axs1[1].set_xticks(x + width, error_ranges, fontsize = 20)
axs1[1].set_ylim([0,20])
axs1[1].legend(fontsize = 20)

# fig1.tight_layout()
fig1.savefig('total_rel_error_details.jpg',dpi = 400)

#%% Age class distribution check:
age_class_eureca = ['< 1930', '1930-1945', '1946-1960', '1961-1976', '1977-1991', '1992-2005', '>2005']
age_class_eureca_dist = [2141/30886, 1387/30886, 6137/30886, 12380/30886, 5682/30886, 2790/30886, 369/30886]
# From ISTAT database

fig1, axs1 = plt.subplots(2, figsize = (19,9.5))

# create new vector with complete distribution:
distr_489_orig_geom = age_class_distribution(ED_489_orig_geom_rnd_age_district, 0)
distr_2059_orig_geom = age_class_distribution(ED_2059_orig_geom_rnd_age_district, 0)


error_ranges = (age_class_eureca)
error_values = {
    '489 buildings': [round(x,3)*100 for x in list(distr_489_orig_geom.values())],
    '2059 buildings': [round(x,3)*100 for x in list(distr_2059_orig_geom.values())],
    'ISTAT reference': [round(x,3)*100 for x in age_class_eureca_dist],
}
    
x = np.arange(len(error_ranges))  # the label locations
width = 0.20  # the width of the bars
multiplier = -0.05

for attribute, measurement in error_values.items():
    offset = width * multiplier
    rects = axs1[0].bar(x + offset, measurement, width, label=attribute)
    axs1[0].bar_label(rects, padding=3, rotation = 'vertical')
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
axs1[0].set_xlabel('Age Class')
axs1[0].set_ylabel('Belonging %')
axs1[0].set_title('Age Class distribution comparison')
axs1[0].set_xticks(x + width, error_ranges)
axs1[0].set_ylim([0, 80])
axs1[0].legend()

fig1.tight_layout()
fig1.savefig('age_class_distribution_check.jpg',dpi = 400)

#%% Comparison between 489 pre and post age geometry modification (error distribution comparison):
fig1, axs1 = plt.subplots(2, figsize = (19,9.5))

error_ranges = ('[-1.0 ; -0.75[', "[-0.75 ; -0.5[", "[-0.5 ; -0.25[", '[-0.25 ; 0[', '[0 ; 0.25[', '[0.25 ; 0.5[', '[0.5 ; 0.75[', '[0.75 ; 1.0[', '[1.0 ; 1.25[', '[1.25 ; 1.5[', '[1.5 ; +inf[')

vector_mod_geom = remove_inf(ED_489_mod_geom_manual_age['output_analysis_df']['relative_error_2020'])
vector_orig_geom = remove_inf(ED_489_orig_geom_manual_age['output_analysis_df']['relative_error_2020'])

error_values = {
    'Mod geom': [round((x *100 / len(vector_mod_geom)),1) for x in count_values_in_range(error_ranges, ED_489_mod_geom_manual_age['output_analysis_df']['relative_error_2020'])],
    'Orig geom': [round((x *100 / len(vector_orig_geom)),1) for x in count_values_in_range(error_ranges, ED_489_orig_geom_manual_age['output_analysis_df']['relative_error_2020'])],
    }

x = np.arange(len(error_ranges))  # the label locations
width = 0.35  # the width of the bars
multiplier = 0.5

for attribute, measurement in error_values.items():
    offset = width * multiplier
    rects = axs1[0].bar(x + offset, measurement, width, label=attribute)
    axs1[0].bar_label(rects, padding=3, )
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
axs1[0].set_xlabel('Intervallo di errore relativo')
axs1[0].set_ylabel('% edifici')
axs1[0].set_xticks(x + width, error_ranges)
axs1[0].set_ylim([0, 30])
axs1[0].legend()

#%% comparison among different age class, same dataset:
fig1, axs1 = plt.subplots(2, figsize = (19,9.5))

error_ranges = ('[-1.0;-0.75[', "[-0.75;-0.5[", "[-0.5;-0.25[", '[-0.25;0[', '[0;0.25[', '[0.25;0.5[', '[0.5;0.75[', '[0.75;1.0[', '[1.0;1.25[', '[1.25;1.5[', '[1.5;+inf[')

vector_fixed = remove_inf(ED_2059_orig_geom_fixed_age['output_analysis_df']['relative_error_2020'])
vector_random = remove_inf(ED_2059_orig_geom_rnd_age_city['output_analysis_df']['relative_error_2020'])
vector_PRG = remove_inf(ED_2059_orig_geom_rnd_age_district['output_analysis_df']['relative_error_2020'])

error_values = {
    'Età fissa': [round((x *100 / len(vector_fixed)),1) for x in count_values_in_range(error_ranges, ED_2059_orig_geom_fixed_age['output_analysis_df']['relative_error_2020'])],
    'Età random (ISTAT 2011)': [round((x *100 / len(vector_random)),1) for x in count_values_in_range(error_ranges, ED_2059_orig_geom_rnd_age_city['output_analysis_df']['relative_error_2020'])],
    'Età PRG': [round((x *100 / len(vector_PRG)),1) for x in count_values_in_range(error_ranges, ED_2059_orig_geom_rnd_age_district['output_analysis_df']['relative_error_2020'])],
    }

x = np.arange(len(error_ranges))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0.0

for attribute, measurement in error_values.items():
    offset = width * multiplier
    rects = axs1[0].bar(x + offset, measurement, width, label=attribute)
    axs1[0].bar_label(rects, padding=3, rotation = 90)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
axs1[0].set_xlabel('Intervallo di errore relativo')
axs1[0].set_ylabel('% edifici')
axs1[0].set_xticks(x + width, error_ranges)
axs1[0].set_ylim([0, 30])
axs1[0].legend()











