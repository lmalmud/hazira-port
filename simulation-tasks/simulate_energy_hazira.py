'''
simulate_energy_hazira.py
Hourly kWh draw base 6 500; 
+27 % peak (08–18 h); 
seasonal ±17 % (summer/winter); 
add 6 % ad- min/lighting overhead.
'''

import csv
import numpy as np

data = []

with open('energy_consumption_hazira.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(data)