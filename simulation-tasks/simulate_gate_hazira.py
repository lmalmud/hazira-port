'''
simulate_gate_hazira.py
Generate 160 trucks/day (Poisson), 
service μ = 11min, σ = 2.5min; 
apply peak-hour surge +28 % 
(08–10 h, 17–19 h);
output queue lengths.

There is only one gate, so one truck can be processed at a time.
The time that it takes for a truck to be processed is normally distributed
with mean 11 and standard deviation 2.5.
We would like to track the number of trucks in the queue at each hour.

Note that all time values are measured in hours

Sanity check:
We expect a total number of procesisng hours to be: 160*(11/60)
So, we expect (160*(11/60)-24)/(11/60) = 29 remaining trucks at the end of the simulation
'''

import csv
import numpy as np
import pandas as pd

SIM_START = pd.to_datetime('2025-01-01 00:00')
SIM_END = SIM_START + pd.Timedelta(days=365)

class Truck:
    '''
    A class to represent the trucks that will arrive at the gate.
    '''

    def __init__(self, arrival_time):
        self.arrival_time = arrival_time

        # The number of minutes it takes to service is 6 at minimum, otherwise normally distributed
        service_mins = max(6, np.random.normal(loc=11, scale=2.5, size=1)[0])
        self.service_time = pd.Timedelta(minutes=service_mins)
        self.completion_time = pd.NaT # Updated once the truck has been processed

    def __str__(self):
        '''
        Returns a string representing the truck,
        stating the arrival and service times.
        '''
        return f'TRUCK. arrival_time: {self.arrival_time.isoformat()}, service_time: {self.service_time}'

class Gate:
    '''
    A class to represent the gate, which may have a queue
    of trucks waiting to be processed.
    '''

    def __init__(self):
        self.queue = []

    def add(self, truck):
        '''
        Enqueues a truck at the gate by appending
        it to the internal queue
        '''
        self.queue.append(truck)

    def update(self, time_now, duration):
        '''
        Updates the internal queue of trucks by
        removing trucks that have been processed and
        decrementing remaining service time knowing that
        it has been duration hours since the last update
        Parameters
        time: current time (in hours)
        Returns
        number of trucks processed
        '''
        remaining = duration
        completed = 0

        # If there are still trucks that must be processed and more processing time
        while remaining > pd.Timedelta(0) and self.queue: 

            head = self.queue[0] # Next truck to be processed

            # If we can process this truck entirely, with time to spare
            if head.service_time <= remaining:

                # The time it took to finish was the time at start (time)
                # plus the amount of processing time that has already occred
                head.completion_time = time_now + (duration - remaining)

                # Update reamining time, note not all time was used
                remaining -= head.service_time

                self.queue.pop(0)

                completed += 1

            # All of the processing time had to be used on the first truck
            else:
                head.service_time -= remaining
                remaining = pd.Timedelta(0)

        return completed

'''
We would like a new row in the spreadsheet when any event occurs. This could be:
- The arrival of a new truck
- The processing of one truck completes

We will allow for trucks to arrive any quarter hour, so the number of trucks per hour is:
regular: poisson ~ 160/(24*4)
peak: poisson ~ 160*1.28/(24*4)

The simulation will be processed in quarter hours.
'''
HOUR_TIMESTEP = 4 # The number of intervals per hour
TICK = pd.Timedelta(hours=1/HOUR_TIMESTEP)

# [time (in hours), arrivals, queue_length]
data = [['time', 'arrivals', 'num_processed', 'queue_length']]

time = SIM_START # The current simulation time
gate = Gate() # A gate object to process trucks

deps = 0 # The number of departed trucks since the last tick
arrivals = 0 # The number of arrivals since the last tick

# Run the simulation for 24 hours
while time < SIM_END:
    # Draw the number of trucks from a poisson distribution
    num_trucks = np.random.poisson(lam = 160/(24*HOUR_TIMESTEP), size=1)[0]

    hr = time.hour # Get the current hour of the simulation

    # If it is during a peak time, adjust the poisson parameter
    if (8 <= hr and hr <= 10) or (17 <= hr and hr <= 19): 
        num_trucks = np.random.poisson(lam = 160*1.28/(24*HOUR_TIMESTEP))

    arrivals += num_trucks

    # Add one new truck to the gate for each of the trucks to be added this interval
    for i in range(num_trucks):
        gate.add(Truck(time))

    time += TICK
    deps += gate.update(time, TICK)
    if time.minute == 0: # Only write data on the hour
        data.append([time, arrivals, deps, len(gate.queue)])
        deps = 0
        arrivals = 0

# Write output to csv file
with open('gate_entries_hazira.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(data)