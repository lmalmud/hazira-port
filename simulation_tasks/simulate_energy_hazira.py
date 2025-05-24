'''
simulate_energy_hazira.py
Hourly kWh draw base 6 500; 
+27 % peak (08–18 h); 
seasonal ±17 % (summer/winter); 
add 6 % admin/lighting overhead.

kWh = kilowatt-hour

Base draw 6500 kWh/hr: the typical energy draw
Peak-hour surge draws 6500*1.27 during these hours
In summer, we require 17% more energy
In winter, we require 17% less energy
Every draw is increased by 6% of what it usually

Note that this simulation is deterministic- could adjust to draw
each energy usage from a Normal with mean energy.
'''

import csv
import numpy as np
import pandas as pd # Used for ease in handling dates

data = [['time', 'energy_kWh']]
# Generate dates from Jan 1 to Dec 31, hourly data
for timestamp in pd.date_range('2025-01-01 00:00', '2025-12-31 23:00', freq='h'):
    h, m = timestamp.hour, timestamp.month # Record current hour and month

    # Increase by 27% if during peak hours
    peak_hour_factor = 1.27 if 8 <= h <= 18 else 1

    # Summer is June, July, August (6, 7, 8) so +17%
    # Winter is December, January, February (12, 1, 2) so -17%
    season_factor = 1.17 if m in [6, 7, 8] else (.83 if m in [12, 1, 2] else 1)
    
    # Calculate adjusted energy used, accounting for the admin factor of 1.06
    energy = round(6500 * 1.06 * peak_hour_factor * season_factor, 2)
    data.append([timestamp, energy])

# Write output to csv file
with open('energy_consumption_hazira.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(data)