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

# Read the data from previous vessel arrival simulation
container_arrival = []
with open("vessel_turnaround_hazira.csv", 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        container_arrival.append(row)
container_arrival = container_arrival[1:]

# There are 6 quay cranes
data = []
for container in container_arrival:
    # Draw the number of moves from poisson(lambda=2.6) and round the result
    num_moves = round(np.random.poisson(lam=2.6)[0])

    # TODO: add movement simulation

with open('container_moves_hazira.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(data)