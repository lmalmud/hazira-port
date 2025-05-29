'''
simulate_berth_hazira.py
Write simulate berth hazira.py:
generate 365 days of berth-level oc-
cupancy at 78 % avg utilization,
with monsoon dip (–14% Jul–Sep)
and winter peak (+9 % Dec–Feb).
'''

import csv # Used for writing to the output file
import numpy as np # Used for simulating draws from the Normal distribtuion
import pandas as pd # For dates
import matplotlib.pyplot as plt # For heatmap

SHOW_FIG = False

# Data will eventually be written to .csv
data = []
data.append(['time', 'MP1', 'MP2', 'MP3', 'MP4', 'CT1', 'CT2'])

heatmap_values = []

for timestamp in pd.date_range('2025-01-01 00:00', '2025-12-31 23:00', freq='D'):
    month = timestamp.month
    mean = .78
    if month in [7, 8, 9]: # Monsoon dip
        mean = .78 - .14
    if month in [12, 1, 2]: # Winter peak
        mean = .78 + .09

    occupancy = np.random.normal(loc=.78, scale=.05, size=6).tolist()
    occupancy = [round(x, 2) for x in occupancy]

    heatmap_values.append(occupancy)
    data.append([timestamp.isoformat()] + occupancy)

with open('berth_occupancy_hazira.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(data)

if SHOW_FIG:
    plt.figure(figsize=(12,4))
    plt.title('Berth Occupancy Over Year')
    plt.xlabel("Day (of 365)")
    plt.ylabel("Berth (MP1-MP4, CT1-2)")
    plt.imshow(np.transpose(heatmap_values), cmap="viridis", aspect="auto")
    plt.colorbar() # Show color keys
    plt.show()
