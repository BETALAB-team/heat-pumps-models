## Introduction 
This manual descripes the workflow for heat pump performance models together with the validation scripts against international standards. 

## Repository Structure 
The repository is organzied into following main parts: 

1. Original Code folder which contains the legacy codes used for the publication at UIT Conference 2025. 
2. Clean Code folder which contains the cleaned models with the most recent changes for calculation of heat pump performances. 
3. Test with standards which containst the scripts to validate against the following standards:
- *ISO 13612-2*
- *EN 14825* 

$Note:$ scrips namde in the format "New_models_..." are not cleaned and they contain the comments that can help the further analysis. 

## Prerequisites 
To eecute the model, the following foders must exist in the working directory. 

1. Data Folder: 
a folder named "Data" which includes: 
An excel file with the same name as the heat pump unit with two sheets:

- Full load: contains the catalogue points in full load operation 
- SetData 
Contains data in partial and full load operation 

Catalogure points shall include the following columns: 

    * SET [°C] : Source entering temperature 
    * LET [°C] : Load entering temperature 
    * LExT [°C] : Load exiting temperature
    * Pow [kW] :  electrical power absorbed 
    * Heat Cap CPND [kW]: heating capacity of the heat pump 
    * PLR: partial load ratio defined as the heat capacity divided by the heat capacity at full load
    * COP: coefficient of performance 
    * Heat Cap COND full [kW]: the heating capacity at the full load regime 
    * Pow full [kW] : electrical power absorbed at the full load regime

2. ExpData Folder which includes: 
* A file containing eperimental points which is organized as functions of Temperatures and PLR. Experimental data from HeatpumpMonitor can be downloaded using the script 
> download_timeseries.py 


## Simulation procedure
The main simulation file is the script 
> Test_classes.py 

to use this script the heat pump device shall be defined as a tuple with three variables: device = (exp, cat, type)

* exp is the name of the file that includes the experimental points
  
* cat is the name of the file that includes the catalogue data
  
* type can be AtW or WtW based on the type of the heat pump, whether it is air to water or water to water. 

In order to execute the model, you need to define the heat pump object: 

> HP = HeatPump(device)

then you can identify the working regimes and the full load conditions:
> HP.status_analysis()

> HP.interp_full_load()

at this point the heat pump object will have its operating regimes determined. and you can fit and validate the model.

> HP.new_model_fit() 

## Results 
after executions, you can save the generated KPI.csv and use the dedicated script to generate result plots: 

> Plot_classes.py 


## Citation 
The methodology in this repository is described in the following article: 

@article{Bena2026HPMethod,
  author  = {Benà, Francesco and Khajedehi, Mohamad Hasan and Vivian, Jacopo and Zarrella, Angelo},
  title   = {A method to evaluate the energy performance of inverter-driven heat pumps in real operating conditions},
  journal = {Applied Thermal Engineering},
  year    = {2026},
  doi     = {10.1016/j.applthermaleng.2026.130133}
}


