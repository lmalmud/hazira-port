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
        self.yard_arrival = start_time
        self.move_start_time = 0 # Time that the move is able to begin
        # Note that move_start_time may not be equal to yard_arrival because
        # the container may not be able to be processed immediately
        self.move_end_time = 0
        self.resource_name = '' # The resource that the movement will occur at e.g. Yard2

    def __str__(self):
        return f'MOVE. yard arrival: {self.yard_arrival}, at {self.resource_name} move start: {self.move_start_time}, move end: {self.move_end_time}'

class YardResource:
    '''
    A class that represents a particular resource in the yard
    that will perform a 'move' on containers.
    '''

    def __init__(self, type='Quay', name=''):
        self.type = type # Either Yard or Quay
        self.name = name # Label for this particular crane later used in the output files
        self.containers = [] # List of containers that need to be processed
        self.next_idle_time = 0

    def process(self, container):
        '''
        Simulates the processing of a container at the given yard resource.
        The duration of the processing time is dependent upon whether the particular
        crane is Yard/RTG or a Quay. The container is either processed immediately,
        if the crane is currently idle, or processed immediately upon the next time
        the crane is free.
        '''
        # If quay, processing time is normal with mean 90s, standard dev 10s
        # Truncate at 20 seconds
        processing_time = max((20/(60*60)), np.random.normal(loc=(90/(60*60)), scale=(10/(60*60)), size=1)[0])

        # If yard, processing time is normal with mean 144s, standard dev 15s
        # Truncate at 30s
        if self.type == 'Yard':
            processing_time = max((30/(60*60)), np.random.normal(loc=(144/(60*60)), scale=(15/(60*60)), size=1)[0])
        
        # If the next container to be processed is after the next idle time
        if container.yard_arrival > self.next_idle_time:
            self.next_idle_time += container.yard_arrival + processing_time
            container.move_start_time = container.yard_arrival
            
        # May process immediately
        else:
            container.move_start_time = self.next_idle_time
            self.next_idle_time += processing_time

        # Update the properties of the container that track its movement
        container.move_end_time = container.move_start_time + processing_time
        container.resource_name = self.name

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
    resources.append(YardResource('Quay', name=f'Quay{i}'))
for i in range(14):
    resources.append(YardResource('Yard', name=f'Yard{i}'))

# data will be what is written to the csv file ultimately
data = [['container_arrival', 'resource_assigned', 'move_start', 'move_end']]

# A list of every move that occurs at the port (data in the output csv will be extracted from these objects)
all_moves = []
for container in container_arrival:
    # Draw the number of moves from poisson(lambda=2.6) and round the result
    num_moves = round(np.random.poisson(lam=2.6))

    # container = [arrival_time, berth_id, service_time, delay_flag, start_time, end_time]
    for i in range(num_moves):
        # the start time of the move is the end_time of when it was processed at the berth
        current_move = ContainerMove(float(container[5]))

        # TODO: add movement simulation
        resource_to_add = resources[0]
        for resource in resources:
            if resource.next_idle_time < resource_to_add.next_idle_time:
                resource_to_add = resource

        # This method will update the properties of the move
        resource_to_add.process(current_move)
        all_moves.append(current_move)

# Write all relevant simulation information to data list
for move in all_moves:
    # [container_arrival, resource_assigned, move_start, move_end]
    data.append([move.yard_arrival, move.resource_name, move.move_start_time, move.move_end_time])

with open('container_moves_hazira.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(data)