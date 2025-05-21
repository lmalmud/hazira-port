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

# Defining the parameters and scale for the Weibull draws
k = 1.7
mean_interarrival = 12
lambda_scale = mean_interarrival / mp.gamma(1 + 1/k)

class Crane:
    def __init__(self, name, downtime):
        self.name = name
        self.downtime = downtime
        self.failures = []
    
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
        # FIXME
        pass

cranes = []
# There are 6 quay cranes and 14 yard (RTG) cranes
for i in range(6):
    cranes.append(Crane(name=f'Quay{i}', downtime=1.2))
for i in range(14):
    cranes.append(Crane(name=f'Yard{i}', downtime=1))

for crane in cranes:
    # Simulate failures on this crane until one year has been simulated
    simulation_time = 0 # Measured in hours
    while simulation_time < 365*24:
        # Randomly generate the time between failures
        next_failure = np.random.weibull(1.7, size=1)[0] * lambda_scale

        # Increment simulation time to the next failure
        simulation_time += next_failure
        
        crane.fail(simulation_time)

# [resource_name, downtime_start, downtime_end]
data = []

with open('crane_uptime_hazira.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(data)