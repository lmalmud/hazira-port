'''
apply_scenario_hazira.py
Apply each scenario’s multipliers to S1–S11 outputs; 
output adjusted CSVs per scenario.
'''

import json
import pandas as pd

def scale_timedelta(x, multiplier):
    '''
    Scales a timedelta object (in string format) by a multiplier
    Parameters
    x: string of pd.timedelta
    multiplier: float
    Returns
    pd.timedelta
    '''
    return pd.to_timedelta(pd.to_timedelta(x).total_seconds() * multiplier, unit='s').round('s')

def improve_gate(num_processed, queue_length, multiplier):
    return 1

# Read the .json file that defines the improvement metrics
scenarios = []
with open('Scenario_Parameters_Hazira.json', 'r') as file:
    scenarios = json.load(file)

# Read in the appropriate dataframes which we will apply improvements to
vessel_turnaround = pd.read_csv('../simulation_tasks/vessel_turnaround_hazira.csv')
crane = pd.read_csv('../simulation_tasks/crane_uptime_hazira.csv')
gate = pd.read_csv('../simulation_tasks/gate_entries_hazira.csv')

for scenario in scenarios['scenarios']:

    # Scales the service time of each vessel by the appropriate multiplier
    # Note that an x% improvement is scaling the service time by (1-x/100),
    # so the parameters in .json file are given in such format
    turnaround = vessel_turnaround['service_time'].apply(
        lambda x : scale_timedelta(x, scenario['multipliers']['vessel_service_time'])) # Berth turnover
    
    # The simulation tracks only the time that the cranes are down, so we would like
    # to reduce each downtime, by scaling it down
    downtime = crane['duration'].apply(
        lambda x : scale_timedelta(x, scenario['multipliers']['crane_downtime']) # Crane productivity
    )

    gate_updated = gate.apply(lambda x : 
        improve_gate(gate['num_processed'], 
                     gate['queue_length'], 
                     scenario['multipliers']['gate_speed']))
    
    df_improvement =  pd.DataFrame({
        'vessel_service_time' : turnaround,
        'crane_downtime' : downtime,
        'gate_processed' : gate_updated
    })
    sim_name = scenario['name']
    df_improvement.to_excel(f'hazira_{sim_name}_scenario.xlsx')

