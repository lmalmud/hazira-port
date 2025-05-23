'''
ingest_maintenance_events_hazira.py
Enforces schema for maintenance_events_hazira.csv
'''

from enforce_schema import enforce_schema
import pandas as pd

SCHEMA = {
    'columns' : ['time', 'resource', 'maintenance_duration'],
    'dtypes' : {'time' : 'datetime64[ns]',
                'resource' : 'string',
                'maintenance_duration' : 'timedelta64[ns]'}
}

file = '../simulation_tasks/maintenance_events_hazira.csv'
enforce_schema(file, 'maintenance_events_hazira', SCHEMA)