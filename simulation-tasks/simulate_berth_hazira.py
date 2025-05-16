'''
simulate_berth_hazira.py
Write simulate berth hazira.py:
generate 365 days of berth-level oc-
cupancy at 78 % avg utilization,
with monsoon dip (–14% Jul–Sep)
and winter peak (+9 % Dec–Feb).
'''

import csv

# List of names of all months
months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

# List of month names that have only 30 days
thirty_days = ['September', 'April', 'June', 'November']

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
        data.append(f'{month_to_number[month]}/{i}')

print(data)