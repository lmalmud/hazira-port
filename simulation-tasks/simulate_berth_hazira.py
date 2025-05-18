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

# List of names of all months
months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

# List of month names that have only 30 days
thirty_days = ['September', 'April', 'June', 'November']

# Months with monsoon dip (-14%) and winter peak (+9%)
monsoon_dip = ['July', 'August', 'September']
winter_peak = ['December', 'January', 'February']

# Dictionary to convert month to numerical value
month_to_number = {'January' : 1, 'February' : 2, 'March' : 3, 'April': 4,
                   'May' : 5, 'June' : 6, 'July' : 7, 'August' : 8, 'September' : 9,
                   'October' : 10, 'November' : 11, 'December' : 12}

# Build list of strings of form 'month/day'
data = []
for month in months:
    bound = 31 # Number of days to add for this month
    if month in thirty_days:
        bound = 30

    for i in range(1, bound+1): # For each day, append a string with day/month
        current_row = []
        current_row.append(f'{month_to_number[month]}/{i}')

        # If it is not a peak or dip, we use 78% utilization
        # loc is mean, scale is standard deviation
        occupancy = float(np.random.normal(loc=.78, scale=.05, size=1)[0])
        
        if month in monsoon_dip: # -14%
            occupancy = float(np.random.normal(loc=.78-.14, scale=.05, size=1)[0])
        if month in winter_peak: # +9%
            occupancy = float(np.random.normal(loc=.78+.09, scale=.05, size=1)[0])

        current_row.append(occupancy)

        data.append(current_row)

with open('simulate_berth_hazira.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(data)