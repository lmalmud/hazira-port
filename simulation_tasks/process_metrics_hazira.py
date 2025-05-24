'''
process_metrics_hazira.py
Aggregate S1–S8 outputs into monthly metrics: 
berth idle hrs, avg vessel turnaround, 
TEU moves, crane downtime hrs, 
trucks processed, kWh consumption.
'''

import csv
import pandas as pd
import numpy as np
import math

# METRIC 1: berth idle hours
# [arrival_time,berth,service_time,delay_flag,start_time,end_time]
vessel_turnaround = []
with open('vessel_turnaround_hazira.csv', 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        vessel_turnaround.append(row)
vessel_turnaround = vessel_turnaround[1:]

# Create a dataframe that will store the information
BERTHS = ['MP1', 'MP2', 'MP3', 'MP4', 'CT1', 'CT2']
idx = pd.date_range('2025-01-01 00:00', '2025-12-31 23:00', freq='h')
df_occ = pd.DataFrame(
    0, # fill with zeros
    index=idx, # index the dataframe by dates
    columns=BERTHS # columns will be names of berths
)

# For each row in the csv, representing an arrived vessel
for vessel in vessel_turnaround:
    # Obtain the start and end hours by rounding down the start and end time of the vessel's processing
    start_hour = pd.to_datetime(vessel[4]).floor('h')
    end_hour= pd.to_datetime(vessel[5]).floor('h')

    # Get list of all hours that overlap with start and end range
    hours = pd.date_range(start_hour, end_hour, freq='h').intersection(df_occ.index)
    df_occ.loc[hours, vessel[1]] = 1

# Only get the part of the dataframe that is the berths
df_berths = df_occ[['MP1', 'MP2', 'MP3', 'MP4', 'CT1', 'CT2']].astype(int)

idle_hours = (1 - df_berths).sum(axis=1).resample('ME').sum() # If we only care about total idle hours
# idle_hours = (1 - df_berths).resample('ME').sum() # If we want to separate by berth

# METRIC 2: average vessel turnaround
df_vessel = pd.read_csv('vessel_turnaround_hazira.csv')

# Need to convert some columns to be parsed as datetime objects
df_vessel['arrival_time'] = pd.to_datetime(df_vessel['arrival_time'])
df_vessel['start_time'] = pd.to_datetime(df_vessel['start_time'])
df_vessel['end_time'] = pd.to_datetime(df_vessel['end_time'])

# Create the turnaround column as the difference between end and start times, in hours
df_vessel['turnaround'] = (
    df_vessel['end_time'] 
  - df_vessel['start_time']
).dt.total_seconds() / 3600

# .resample will group by months (ME) but not using the usual index column, but rather the times in arrival_time
avg_turn = df_vessel.resample('ME', on='arrival_time').turnaround.mean()

# METRIC 3: TEU moves
df_moves = pd.read_csv('container_moves_hazira.csv')
df_moves['container_arrival'] = pd.to_datetime(df_moves['container_arrival'])
df_calls = (
    df_moves[['call_id','container_arrival','teu_handled']]
      .drop_duplicates(subset='call_id') # Only want the teu handled once per vessel
      .set_index('container_arrival') # Want to choose montly metrics by the arrival time
)

# Find the total number of TEU moved
monthly_teu_moves = df_calls['teu_handled'].resample('ME').sum()

# METRIC 4: crane downtime hours
df_crane = pd.read_csv('crane_uptime_hazira.csv')
# Convert start and end to be datetime objects
df_crane['downtime_start'] = pd.to_datetime(df_crane['downtime_start'])
df_crane['downtime_end'] = pd.to_datetime(df_crane['downtime_end'])
# Calculate the duration of each downtime
df_crane['duration'] = df_crane['downtime_end'] - df_crane['downtime_start']
# Calculate total monthly downtime
crane_downtime_quay = df_crane[df_crane['resource_name'].str.startswith('Quay')].resample('ME', on='downtime_start').duration.sum()
crane_downtime_yard = df_crane[df_crane['resource_name'].str.startswith('Yard')].resample('ME', on='downtime_start').duration.sum()

# METRIC 5: trucks processed
df_trucks = pd.read_csv('gate_entries_hazira.csv')
df_trucks['time'] = pd.to_datetime(df_trucks['time']) # Convert timestamps to pandas objects

# Calculate the sum of trucks processed within each month
trucks_proc = df_trucks.resample('ME', on='time').num_processed.sum()

# METRIC 6: kWh consumption
df_energy = pd.read_csv('energy_consumption_hazira.csv')
df_energy['time'] = pd.to_datetime(df_energy['time'])

# Find total amount of energy per month
kwh_monthly = df_energy.resample('ME', on='time').energy_kWh.sum()

# EXPORT to .xlsx
df_monthly = pd.DataFrame({
  'berth_idle_hrs': idle_hours,
  'avg_vessel_turnaround_hrs': avg_turn,
  'monthly_TEU': monthly_teu_moves,
  'quay_crane_downtime_hrs': crane_downtime_quay,
  'yard_crane_downtime_hrs' : crane_downtime_yard,
  'trucks_processed': trucks_proc,
  'kwh_consumption': kwh_monthly
})

# Need to conver the index to string format so that it displays in Excel
df_monthly.index = df_monthly.index.strftime('%Y-%m-%d %H:%M:%S')
df_monthly = df_monthly.iloc[:-1] # Remove last row which has some data from the next year
df_monthly.to_excel('hazira_monthly_metrics.xlsx')
