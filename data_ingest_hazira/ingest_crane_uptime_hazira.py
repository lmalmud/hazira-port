'''
ingest_crane_uptime_hazira.py
Enforces schema for crane_uptime_hazira.csv
'''

from enforce_schema import enforce_schema
import pandas as pd

SCHEMA = {
    'columns' : ['resource_name', 'downtime_start', 'downtime_end'],
    'dtypes' : {'resource_name' : 'string',
                'downtime_start' : 'datetime64[ns]',
                'downtime_end' : 'datetime64[ns]'}
}

file = '../simulation_tasks/crane_uptime_hazira.csv'
enforce_schema(file, 'crane_uptime_hazira', SCHEMA)