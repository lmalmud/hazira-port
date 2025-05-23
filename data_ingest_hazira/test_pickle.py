'''
test_pickle.py
Reads the pickled dataframes to ensure
that they were recorded properly
'''

import pandas as pd

# ingest_berth_occupancy_hazira.py
berth = pd.read_pickle('berth_occupancy_hazira.pkl')

# ingest_container_moves_hazira.py
container = pd.read_pickle('container_moves_hazira.pkl')

# ingest_crane_uptime_hazira.py
crane = pd.read_pickle('crane_uptime_hazira.pkl')

# ingest_energy_consumption_hazira.py
energy = pd.read_pickle('energy_consumption_hazira.pkl')

# ingest_gate_entries_hazira.py
gate = pd.read_pickle('gate_entries_hazira.pkl')

# ingest_maintenance_events_hazira.py
maintenance = pd.read_pickle('maintenance_events_hazira.pkl')
print(maintenance)