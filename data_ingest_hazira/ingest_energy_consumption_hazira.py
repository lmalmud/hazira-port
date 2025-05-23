'''
ingest_energy_consumption.py
Enforces schema for energy_consumption_hazira.csv
'''

from enforce_schema import enforce_schema
import pandas as pd

SCHEMA = {
    'columns' : ['time', 'energy_kWh'],
    'dtypes' : {'time' : 'datetime64[ns]',
                'energy_kWh' : 'float64'}
}

file = '../simulation_tasks/energy_consumption_hazira.csv'
enforce_schema(file, 'energy_consumption_hazira', SCHEMA)