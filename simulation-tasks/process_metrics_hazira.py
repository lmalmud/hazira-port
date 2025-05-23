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

# A dictionary that will hold the hours that each berth is occupied
BERTHS = {'MP1' : [], 'MP2' : [], 'MP3':[], 'MP4':[] , 'CT1':[], 'CT2':[]}

for vessel in vessel_turnaround:
    # Obtain the start and end hours by rounding down the start and end time of the vessel's processing
    start_hour = math.floor(float(vessel[4]))
    end_hour= math.floor(float(vessel[5]))

    # For each hour in that range, mark the berth as being occupied
    for i in range(start_hour, end_hour+1):
        BERTHS[vessel[1]].append(i) # Access the berth by its key, which is its ID

# An array that will store the raw occupancy data
# The first column will be hourly timestamps
occ_data = [[timestamp for timestamp in pd.date_range('2025-01-01 00:00', '2025-12-31 23:00', freq='h')]]

# Iterate over each of the berths
for berth in BERTHS.keys():
    current = []

    # For every hour in the year
    for i in range(365*24):
        # Add 1 if the berth is occupied at this hour and zero otherwise
        current.append(int(i in BERTHS[berth]))
    occ_data.append(current)

# We would like each column of the dataframe to be data from one berth, so transpose
numpy_occ = np.array(occ_data).T

# Create a dataframe that will store the information
df_occ = pd.DataFrame(columns=['time']+list(BERTHS.keys()), data=numpy_occ)

# Set the index to be the time column, and cast as an actual datetime opject
df_occ['time'] = pd.to_datetime(df_occ['time'])
df_occ = df_occ.set_index('time')

# Only get the part of the dataframe that is the berths
df_berths = df_occ[list(BERTHS.keys())].astype(int)

# idle_hours = (1 - df_berths).sum(axis=1).resample('ME').sum() # If we only care about total idle hours
idle_hours = (1 - df_berths).resample('ME').sum() # If we want to separate by berth

# METRIC 2: average vessel turnaround