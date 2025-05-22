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
'''

import csv
import numpy as np

class Truck:
    '''
    A class to represent the trucks that will arrive at the gate.
    '''

    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.service_time = np.random.normal(loc=(11/60), scale=(2.5/60), size=1)[0]
        self.completion_time = np.inf # Updated once the truck has been processed

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

    def update(self, time, duration):
        '''
        Updates the internal queue of trucks by
        removing trucks that have been processed and
        decrementing remaining service time knowing that
        it has been duration hours since the last update
        Parameters
        time: current time (in hours)
        Returns
        length of queue
        '''
        while duration > 0:
            if len(self.queue) > 0: # If there are still trucks that must be processed
                self.queue[0].service_time -= duration
                # If it didn't take the entire duration to process this truck
                if self.queue[0].service_time <= 0:
                    # The remaining duration is all time that wasn't used by truck at start of queue
                    duration = abs(self.queue[0].service_time)
                    self.queue.pop(0) # Since there was enough time to complete the task, remove from queue

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

# [time (in hours), queue_length]
data = []

time = 0 # The current simulation time (in hours)
gate = Gate() # A gate object to process trucks

# Run the simulation for 24 hours
while time < 24:
    # Draw the number of trucks from a poisson distribution
    num_trucks = np.random.poisson(lam = 160/(24*HOUR_TIMESTEP), size=1)[0]

    # If it is during a peak time, adjust the poisson parameter
    if (8 <= time and time <= 10) or (17 <= time and time <= 19): 
        num_trucks = np.random.poisson(lam = 160*1.28/(24*HOUR_TIMESTEP))

    # Add one new truck to the gate for each of the trucks to be added this interval
    for i in range(num_trucks):
        gate.add(Truck(time))

    time += 1/HOUR_TIMESTEP
    gate.update(time, HOUR_TIMESTEP)
    data.append([time, len(gate.queue)])