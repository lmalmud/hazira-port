'''
simulate_maintenance_hazira.py
inject weekly planned maint. (3.5 h)
for cranes/RTGs, plus 3 corrective
events/month (4.5 h) across convey-
ors, lighting, berths; tag equipment IDs.

Equipment
- 6 quay cranes (ID Quay1, e.g.)
- 14 RTG/yard cranes (ID Yard2, e.g.)
- MP1-MP4 berths (ID MP1, e.g.)
- CT1-CT2 berths (ID CT1, e.g.)
- Unknown number of conveyors so we will just add one (Conv1)
- Unknown number of lights so we will just add one (Light1)
'''

import csv
import numpy as np
import pandas as pd # For dates
import random

class MaintenanceEvent:
    '''
    A class to represent a maintenance on any port resource.
    '''

    def __init__(self, resource_id, start_time, duration):
        self.resource = resource_id # The name of the resource the maintenance is performed on
        self.start_time = start_time # Start time of maintenance
        self.duration = duration # How long the maintenance will take

    def __str__(self):
        '''
        Return a string to summarize this particular maintenance event.
        '''
        return f'MAINTENANCE on {self.resource} starting at {self.start_time} for {self.duration} hours'


# Define all resources for Hazira port
NUM_QUAY = 6
NUM_YARD = 14
NUM_MP = 4
NUM_CT = 2
NUM_CONVEY = 1
NUM_LIGHT = 1
QUAY = [f'Quay{i}' for i in range(1, NUM_QUAY+1)]
YARD = [f'Yard{i}' for i in range(1, NUM_YARD+1)]
MP = [f'MP{i}' for i in range(1, NUM_MP+1)]
CT = [f'CT{i}' for i in range(1, NUM_CT+1)]
CONVEY = [f'Convey{i}' for i in range(1, NUM_CONVEY+1)]
LIGHT = [f'Light{i}' for i in range(1, NUM_LIGHT)]

# Separate the resources into those with weekly planned maintenace
# and monthly corrective maintenance
WEEKLY_PLANNED = QUAY + YARD
MONTHLY_CORRECTIVE = MP + CT + CONVEY + LIGHT

maintenance_events = []

for resource in WEEKLY_PLANNED: # For each resource that must be maintained weekly
    # Random shift of days to schedule maintenance - will be the same for each resource
    rand_shift = pd.Timedelta(days=random.randint(0, 6))

    # Run through each week in the year
    for timestamp in pd.date_range('2025-01-01 00:00', '2025-12-31 23:00', freq='W'):

        # When the maintenance will be scheduled for
        maintenance_start = timestamp + rand_shift

        maintenance_events.append(MaintenanceEvent(resource, maintenance_start, pd.Timedelta(hours=3.5)))

for resource in MONTHLY_CORRECTIVE:
    # Generate monthly dates (note 's' in 'MS' is for month start)
    for timestamp in pd.date_range('2025-01-01 00:00', '2025-12-31 23:00', freq='MS'):

        # Need to know the number of days in the month in order to pull a random date
        days_in_month = pd.Period(timestamp, freq='M').days_in_month

        # Randomly select three days this month to perform maintenance
        scheduled_days = random.sample(range(0, days_in_month), 3)
        for day in scheduled_days:
            shift = pd.Timedelta(days=day) # Convert the random shift to a pandas Timedelta
            maintenance_start = timestamp + shift # Calculate the random maintenance start

            # Add this event to list of all maintenance events
            maintenance_events.append(MaintenanceEvent(resource, maintenance_start, pd.Timedelta(hours=4.5)))

# Sort events by their start time to prepare to write to .csv
maintenance_events.sort(key = lambda x: x.start_time)

# Aggregate simulation data into rows
data = [['time', 'resource', 'maintenance_duration']]
for event in maintenance_events:
    data.append([event.start_time, event.resource, event.duration])

# Write output to csv file
with open('maintenance_events_hazira.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(data)