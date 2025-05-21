'''
simulate_containers_hazira.py
For each container call (1 500 TEU),
simulate load/unload counts (avg
1400 TEU) and yard moves (2.6 moves/container)
using Hazira yard layouts.

https://www.seavantage.com/blog/what-is-a-port-call-in-ocean-shipping
container call: the arrival of a container vessel at the terminal specifically 
to load and/or unload containers.
TEU = twenty foot equivalent units
So a 1500 TEU container call means that a vessel leaves/departs 
with 1500 standard 20-foot containers

https://blog.intoglo.com/container-yard/
Container Yard (CY) is a designated area within a port or 
terminal where containers are stored before they are loaded 
onto ships or after they have been unloaded.

https://www.cello-square.com/en/blog/view-926.do
moves/container: a single container handling operation within 
the yard—e.g. moving a container from the stack to a truck lane, 
or re‑shuffling stacks.
So each piece of equipment is handled 2.6 times on average during its stay
'''

import csv
import numpy as np

class ContainerMove:
    '''
    A class that will represent one movement of one container.
    '''

    def __init__(self, start_time):
        self.start_time = start_time

class YardResource:
    '''
    A class that represents a particular resource in the yard
    that will perform a 'move' on containers.
    '''

    def __init__(self, type='Quay'):
        self.type = type # Either Yard or Quay
        self.containers = [] # List of containers that need to be processed
        self.next_idle_time = 0

    def process(self, container):
        # If quay, processing time is normal with mean 90s, standard dev 10s
        # Truncate at 20 seconds
        processing_time = min((20/(60*60)), np.normal(loc=(90/(60*60)), scale=(10/(60*60)), size=1)[0])

        # If yard, processing time is normal with mean 144s, standard dev 15s
        # Truncate at 30s
        if self.type == 'Yard':
            processing_time = min((30/(60*60)), np.normal(loc=(144/(60*60)), scale=(15/(60*60)), size=1)[0])
        
        # If the next container to be processed is after the next idle time
        if container.start_time > self.next_idle_time:
            self.next_idle_time += container.start_time + processing_time

        # May process immediately
        else:
            self.next_idle_time += processing_time

        # Add the container to the list of containers handled
        self.containers.append(container)



# Read the data from previous vessel arrival simulation
container_arrival = []
with open("vessel_turnaround_hazira.csv", 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        container_arrival.append(row)
container_arrival = container_arrival[1:]

# There are 6 quay cranes and 14 yard cranes
resources = []
for i in range(6):
    resources.append(YardResource('Quay'))
for i in range(14):
    resources.append(YardResource('Yard'))

data = []
for container in container_arrival:
    # Draw the number of moves from poisson(lambda=2.6) and round the result
    num_moves = round(np.random.poisson(lam=2.6))

    # container = [arrival_time, berth_id, service_time, delay_flag, start_time, end_time]
    for i in range(num_moves):
        current_move = ContainerMove

    # TODO: add movement simulation

with open('container_moves_hazira.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(data)