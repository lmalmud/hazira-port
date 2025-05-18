'''
simulate_vessels_hazira.py
Simulate 1 200 vessel calls/yr
(bulk carriers, container ships, tankers) 
via Poisson arrivals; service μ = 23h, σ = 4.5h; 
include 11 % delay events.

https://www.scribbr.com/statistics/poisson-distribution/
#:~:text=A%20Poisson%20distribution%20is%20a,the%20mean%20number%20of%20events.
A Poisson distribution is a discrete probability distribution.
It gives the probability of an event happening a certain number 
of times (k) within a given interval of time or space.

The Poisson distribution has only one parameter, λ (lambda), 
which is the mean number of events.

So, if there are a mean of 1200 vessel calls/year, we need to convert
those aggregate arrivals to the times at which each vessel arrives.

https://www.probabilitycourse.com/chapter11/11_1_2_
basic_concepts_of_the_poisson_process.php#:~:text=The%20
Poisson%20distribution%20can%20be%20viewed%20as%20the%20limit
%20of%20binomial%20distribution.&text=If%20N(t)%20is%20a%20
Poisson%20process%20with,%E2%8B%AF%20are%20independent%20an
d%20Xi%E2%88%BCExponential(%CE%BB)%2C%20for%20i=1%2C2%2C3%2C%E2%8B%AF.
If there are 1200 vessel calls/year, then the mean time between arrivals
is 1/1200 per year is modeled by an exponential process.

We would like to generate a year's worth of simulated data.
There are 6 berths, so we will assign an arrived vessel to an availabe berth.

We are treating all vessels as the same and not separating by MP1-MP4 and
CT1-CT2 harboring different types of cargo.
'''

class Berth:
    '''
    A class to represent a berth in order to maintain all
    arrivals at that berth.
    '''

    def __init__(self, name):
        # The list of all of the vessels that will arrive at this berth
        self.arrivals = []

        self.name = name

    def dock(self, vessel):
        '''
        Adds a new vessel to the list of arrivals
        '''
        self.arrivals.append(vessel)

    def __str__(self):
        s = self.name + '\n'
        for arrival in self.arrivals:
            s += '\t - ' + str(arrival) + '\n'

class Vessel:
    '''
    A class to represent a vessel that arrives at Hazira
    port.
    '''

    def __init__(self, arrival_time):
        self.arrival_time = arrival_time

        # Service times are distributed normally with mean of 23 and standard deviation 4.5
        self.service_time = np.random.normal(loc=23, scale=4.5, size = 1)
        if self.service_time < 0:
            self.service_time = 1 # If a negative service time is generated, round to 1 hour

        # Generate an 11% chance of whether or not this vessel is delayed
        self.delayed = np.random.binomial(n=1, p=.11, size=1)

        # If this vessel was delayed, increase the service time
        if self.delayed:
            self.service_time += np.random.uniform(.5, 3, size=1)[0]

    def __str__(self):
        return f'VESSEL. arrival time: {self.arrival_time}, service time: {self.service_time}, delayed: {self.delayed}'
        

import csv
import numpy as np
BERTH_NAMES = ['MP1', 'MP2', 'MP3', 'MP4', 'CT1', 'CT2']
ARRIVALS_PER_YEAR = 1200
ARRIVALS_PER_DAY = ARRIVALS_PER_YEAR / 365
ARRIVALS_PER_HOUR = ARRIVALS_PER_YEAR / (365*24)
BERTHS = []
for berth_name in BERTH_NAMES:
    BERTHS.append(Berth(berth_name))

# Count the number of hours that have run in the simulation
time = 0

# These arrivals times represent the time between consecutive arrivals of vessels
arrival_time = time + np.random.exponential(scale=1/ARRIVALS_PER_HOUR, size=1)[0]

# Run while there still have not been 365 days simulated
while arrival_time < 365*24:
    
    # Generate the time of the next arrival
    arrival_time = time + np.random.exponential(scale=1/ARRIVALS_PER_HOUR, size=1)[0]

data = []

with open('vessel_turnaround_hazira.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(data)