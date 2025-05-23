'''
ingest_vessel_turnaround_hazira.py
Enforces schema for vessel_turnaround_hazira.csv
'''

from enforce_schema import enforce_schema
import pandas as pd

SCHEMA = {
    'columns' : ['arrival_time', 'berth', 'service_time', 'delay_flag', 'start_time', 'end_time'],
    'dtypes' : {'arrival_time' : 'datetime64[ns]',
                'berth' : 'string',
                'service_time' : 'timedelta64[ns]',
                'delay_flag' : 'int64',
                'start_time' : 'datetime64[ns]',
                'end_time' : 'datetime64[ns]'}
}

file = '../simulation_tasks/vessel_turnaround_hazira.csv'
enforce_schema(file, 'vessel_turnaround_hazira', SCHEMA)