'''
apply_scenario_hazira.py
Apply each scenario’s multipliers to S1–S11 outputs; 
output adjusted CSVs per scenario.
'''

import json
import pandas as pd
import math

def scale_timedelta(x, multiplier):
    '''
    Scales a timedelta object (in string format) by a multiplier
    Parameters
    x: string of pd.timedelta
    multiplier: float
    Returns
    pd.timedelta
    '''
    #print(pd.to_timedelta(pd.to_timedelta(x).total_seconds() * multiplier, unit='s').round('s'))
    return str(pd.to_timedelta(pd.to_timedelta(x).total_seconds() * multiplier, unit='s').round('s'))

def improve_gate(num_processed, queue_length, multiplier):
    '''
    Applies the improvement multiplier on the number of trucks processed.
    Parameters
    num_processed: int (original number of trucks processed within the frame)
    queue_length: int (number of trucks waiting)
    multiplier: speedup in processing
    Returns
    [new_num_processed, new_queue_length]
    '''

    # Note that we will allow for fractional amounts of processing
    new_num_processed = num_processed * multiplier

    # If the speedup would process more trucks than are currently in the queue
    if new_num_processed - num_processed > queue_length:
        return [queue_length + num_processed, 0]
    else:
        return [new_num_processed, queue_length - (new_num_processed - num_processed)]

# Read the .json file that defines the improvement metrics
scenarios = []
with open('Scenario_Parameters_Hazira.json', 'r') as file:
    scenarios = json.load(file)

for scenario in scenarios['scenarios']:

    # Read in the appropriate dataframes which we will apply improvements to
    # Note that we need to reload these values at the start of each simulation
    vessel_turnaround = pd.read_csv('../simulation_tasks/vessel_turnaround_hazira.csv')
    crane = pd.read_csv('../simulation_tasks/crane_uptime_hazira.csv')
    gate = pd.read_csv('../simulation_tasks/gate_entries_hazira.csv')

    # Scales the service time of each vessel by the appropriate multiplier
    # Note that an x% improvement is scaling the service time by (1-x/100),
    # so the parameters in .json file are given in such format
    vessel_turnaround['service_time'] = vessel_turnaround['service_time'].apply(
        lambda x : scale_timedelta(x, scenario['multipliers']['vessel_service_time'])) # Berth turnover
    
    # The simulation tracks only the time that the cranes are down, so we would like
    # to reduce each downtime, by scaling it down
    crane['duration'] = crane['duration'].apply(
        lambda x : scale_timedelta(x, scenario['multipliers']['crane_downtime']) # Crane productivity
    )

    # For this metric, we need to update both the number of trucks processed at 
    # each step and the queue length
    # Both of these values are returned by improve_gate in a list
    gate['num_processed'] = gate.apply(lambda x : 
        improve_gate(x.num_processed, 
                     x.queue_length, 
                     scenario['multipliers']['gate_speed'])[0], axis=1)
    gate['queue_length'] = gate.apply(lambda x : 
        improve_gate(x.num_processed, 
                     x.queue_length, 
                     scenario['multipliers']['gate_speed'])[1], axis=1)
    
    sim_name = scenario['name'] # moderate, conservative, etc.

    # Note that we need to use "with" otherwise the sheet will not be closed properly
    # We use a writer so that we may rewrite each dataframe as its own sheet
    with pd.ExcelWriter(f'Adjusted_Metrics_SC_{sim_name}.xlsx') as excel_writer:
        vessel_turnaround.to_excel(excel_writer, sheet_name='vessel_turnaround_haizra')
        crane.to_excel(excel_writer, sheet_name='crane_uptime_hazira')
        gate.to_excel(excel_writer, sheet_name='gate_entries_hazira')

'''
An area for expansion would be to add improvement metrics in the other categories
'''