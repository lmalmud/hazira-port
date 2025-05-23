'''
simulate_cranes_hazira.py
quay cranes 19 h uptime/day with 2x1.2 h downtime; 
RTGs (yard) 15h uptime with 2×1 h events;
model failure interarrival via Weibull(k = 1.7).

https://en.wikipedia.org/wiki/Weibull_distribution
Weibull distribution often represents time to failure or 
time between events. k > 1 means that the failure rate
increases with time.

We would like the expected value of something drawn from this distribution to be 12,
so that events occur every 12 hours on average. We can solve for what we need to scale
by: E(T) = \lambda \gamma(1 + \frac{1}{1.7})
so \lambda = \frac{12}{\gamma(1 + \frac{1}{1.7})}
'''

import csv
import numpy as np
import mpmath as mp # for gamma function
import pandas as pd # for time

# Defining the parameters and scale for the Weibull draws
k = 1.7
mean_interarrival = 12
lambda_scale = mean_interarrival / mp.gamma(1 + 1/k)

SIM_START = pd.Timestamp('2025-01-01 00:00')
SIM_END = SIM_START + pd.Timedelta(days=365)

class Crane:
    def __init__(self, name, downtime):
        self.name = name # Name of this crane
        self.downtime = downtime # The hours of failure for each failure
        self.failures = [] # A list of intervals where the crane is not functional
    
    def fail(self, start_time):
        '''
        Adds a failure to the list of failures at the given start time,
        the failure will last as long as the self.downtime parameter specifies
        Parameters
        start_time: hours since start of simulation
        Returns
        none
        '''
        self.failures.append([start_time, start_time + self.downtime])

    def __str__(self):
        '''
        Returns a string representing all relevant data for this crane.
        The name of the crane and its hours of downtime per failure
        followed by a list of every the start and end time of each failure in hours
        '''
        s = f'{self.name} - {self.downtime} hr downtime\n'
        for event in self.failures:
            s += f'\t - {event[0]} - {event[1]}\n'
        return s

cranes = []
# There are 6 quay cranes and 14 yard (RTG) cranes
for i in range(6):
    cranes.append(Crane(name=f'Quay{i}', downtime=pd.Timedelta(hours=1.2)))
for i in range(14):
    cranes.append(Crane(name=f'Yard{i}', downtime=pd.Timedelta(hours=1)))

for crane in cranes:
    # Simulate failures on this crane until one year has been simulated
    simulation_time = SIM_START # Measured in hours
    while simulation_time < SIM_END:
        # Randomly generate the time between failures
        next_failure_hrs = float(np.random.weibull(1.7, size=1)[0] * lambda_scale)
        next_failure = pd.Timedelta(hours=next_failure_hrs).round('s')

        # Increment simulation time to the next failure
        simulation_time += next_failure
        
        crane.fail(simulation_time)

# Each element is of the form [resource_name, downtime_start, downtime_end]
data = [['resource_name', 'downtime_start', 'downtime_end']]

# For each of the cranes, add each failure
for crane in cranes:
    for failure in crane.failures:
        data.append([crane.name, failure[0], failure[1]])

'''
This is a test to see if the total amount of repair time is as expected.
This is a quay crane, so it should fail approximately twice a day for 1.2 hours each time.
So, we expect the accumulated time of failure to be 2.4 hours a day.
accum = 0
for duration in cranes[0].failures:
    accum += duration[1] - duration[0]
print(accum/(365))
'''

# Write output to csv file
with open('crane_uptime_hazira.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(data)