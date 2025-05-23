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
    start_hour = pd.to_datetime(vessel[4]).floor('H')
    end_hour= pd.to_datetime(vessel[5]).floor('H')

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
print(monthly_teu_moves)

# METRIC 4: crane downtime hours
'''
# if df_crane has columns ['timestamp','duration_h']:
crane_downtime = df_crane.resample('M', on='timestamp').duration_h.sum()
'''

# METRIC 5: trucks processed
'''
df_trucks['depart_time'] = …  # if you’ve logged it
trucks_proc = df_trucks.resample('M', on='depart_time').truck_id.count()
'''

# METRIC 6: kWh consumption
'''
kwh_monthly = df_energy.resample('M', on='datetime').adjusted_kwh.sum()
'''

# EXPORT to .xlsx
'''
df_monthly = pd.DataFrame({
  'berth_idle_hrs': idle_hours,
  'avg_vessel_turnaround_hrs': avg_turn,
  'monthly_TEU': monthly_teu,
  'monthly_yard_moves': monthly_moves,
  'crane_downtime_hrs': crane_downtime,
  'trucks_processed': trucks_proc,
  'kwh_consumption': kwh_monthly
})
df_monthly.to_excel('hazira_monthly_metrics.xlsx')
'''
print(df_vessel)