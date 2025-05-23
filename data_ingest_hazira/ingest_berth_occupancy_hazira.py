'''
ingest_berth_occupancy_hazira.py
Enforces schema for berth_occupancy_hazira.csv
'''

from enforce_schema import enforce_schema
import pandas as pd

SCHEMA = {
    'columns' : ['time', 'MP1', 'MP2', 'MP3', 'MP4', 'CT1', 'CT2'],
    'dtypes' : {'time' : 'datetime64[ns]',
                'MP1' : 'float64',
                'MP2' : 'float64',
                'MP3' : 'float64',
                'MP4' : 'float64',
                'CT1' : 'float64',
                'CT2' : 'float64'}
}

file = '../simulation_tasks/berth_occupancy_hazira.csv'
enforce_schema(file, 'berth_occupancy_hazira', SCHEMA)