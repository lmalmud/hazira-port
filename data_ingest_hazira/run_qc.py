'''
run_qc.py
Run quality checks: missingness ¡ 1 %, 
no invalid zeros, flag outliers (¿3σ), 
and produce a PDF report summarizing 
anomalies with charts.
'''

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

TRUNCATE_ROWS = 4 # The maximum number of rows to display in any table

def percent_missing(sim, fig):
    '''
    Creates a bargraph representing the percent of invalid zeros
    for each of the columns that we desire to check for invalid zeros.
    Parameters
    sim: a Simulation object
    fig: the figure to draw the bar graph on
    '''
    percent_missing = []
    for col in sim.df.columns:
        # .isna() will return True of False for missing values
        percent_missing.append(sim.df[col].isna().mean() * 100)
    ax = fig.add_subplot()
    ax.bar(sim.df.columns, percent_missing)
    ax.set_title('Percent Missing Zeros in Each Column')

def invalid_col(sim, fig):
    '''
    For each column to be checked, count the number of elements
    in violation and display some representative values.
    '''
    num_detections = len(sim.invalid_cols.keys()) # The number of checks that will be performed
    count = 1 # Tracks the current row that we will write into
    for col in sim.invalid_cols:
        ax = fig.add_subplot(num_detections, 1, count)
        ax.axis('off')

        # Need to only work with numerical values
        if sim.df[col].dtype == 'timedelta64[ns]':
            sim.df[col] = sim.df[col].dt.total_seconds() / 3600

        # sim.invalid_cols is a dictionary that associates column titles with functions
        # that return true if an entry in that column is invalid
        invalid_rows = sim.df[sim.invalid_cols[col](sim.df[col])]

        if invalid_rows.empty:
            ax.text(.5, .5, f'No invalid entries in {col}', ha='center', va='center', fontsize=12)
        else:
            cell_text = invalid_rows.values.tolist() # 2D array of values
            col_labels = invalid_rows.columns.tolist() # 1D array of column names
            ax.text(.5, .9, f'{len(cell_text)} outlier(s) detected', ha='center', va='center', fontsize=12)
            
            # Truncate displayed outliers if there are more than five
            if len(cell_text) > TRUNCATE_ROWS:
                cell_text = cell_text[:TRUNCATE_ROWS]

            # Display a table
            ax.table(cellText=cell_text, colLabels=col_labels, loc='center')

        count += 1

def outlier_detection(sim, fig, col):
    '''
    Produces a histogram of the values in column and outputs a
    table with a sample of the values that are outliers.
    Parameters
    sim: a Simulation object
    fig: the figure to draw graph and table on
    col: column of sim.df to detect outliers in
    '''
    
    # Calculate the mean and standard deviation of observed values
    mean = sim.df[col].mean()
    std = sim.df[col].std()

    # Find all rows with values that are outliers
    outlier_rows = sim.df[(sim.df[col] < mean - 3 * std) | (sim.df[col] > mean + 3 * std)]
    # Count the number of outliers
    num_outliers = outlier_rows.index.size

    # Need to only work with numerical values
    if sim.df[col].dtype == 'timedelta64[ns]':
        sim.df[col] = sim.df[col].dt.total_seconds() / 3600
    
    ax = fig.add_subplot(2, 1, 1) # 2=nrows, 1=ncols, 1=index (numbered top->bottom, left->right)
    ax.hist(sim.df[col])
    ax.set_title(f'{col} in {sim.name}')

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.axis('off') # Do not show underlying grid

    if outlier_rows.empty:
        ax2.text(.5, .5, "No outliers detected", ha='center', va='center', fontsize=12)
    else:
        ax2.text(.5, .9, f'{num_outliers} outlier(s) detected', ha='center', va='center', fontsize=12)
        cell_text = outlier_rows.values.tolist() # 2D array of values

        # Truncate displayed outliers if there are more than five
        if len(cell_text) > TRUNCATE_ROWS:
            cell_text = cell_text[:TRUNCATE_ROWS]
        
        col_labels = outlier_rows.columns.tolist() # 1D array of column names

        # Display a table
        ax2.table(cellText=cell_text, colLabels=col_labels, loc='center')
    

# Read in dataframes from all simulations
berth = pd.read_pickle('berth_occupancy_hazira.pkl')            # berth_occupancy_hazira.py
container = pd.read_pickle('container_moves_hazira.pkl')        # container_moves_hazira.py
crane = pd.read_pickle('crane_uptime_hazira.pkl')               # crane_uptime_hazira.py
energy = pd.read_pickle('energy_consumption_hazira.pkl')        # energy_consumption_hazira.py
gate = pd.read_pickle('gate_entries_hazira.pkl')                # gate_entries_hazira.py
maintenance = pd.read_pickle('maintenance_events_hazira.pkl')   # maintenance_events_hazira.py
turnaround = pd.read_pickle('vessel_turnaround_hazira.pkl')     # vessel_turnaround_hazira.py

class Simulation:
    '''
    A class that will represent one of the simulations
    and the potential valid datapoints for various components
    of the result
    '''
    def __init__(self, name, df=None, invalid_cols={}, continuous_cols=[]):
        self.name = name

        # The dataframe associated with this simulation
        self.df = df

        # The columns where zero entries are not permissible
        self.invalid_cols = invalid_cols
        
        # The columns that we would like to check for points
        # exceeding three standard deviations
        self.continuous_cols = continuous_cols

# Different functions we will need to determine if a particular value is invalid
def equal_zero(x):
    # Or less than zero would be invalid
    return x <= 0
def neg(x):
    return x < 0
def binary(x):
    return x != 0 or x != 1

SIMULATIONS = [Simulation(name='S2: Berth Occupancy Simulation',
                          df=berth,
                          invalid_cols={'MP1' : equal_zero, 
                                        'MP2' : equal_zero,
                                        'MP3' : equal_zero,
                                        'MP4' : equal_zero,
                                        'CT1' : equal_zero,
                                        'CT2' : equal_zero},
                          continuous_cols=['MP1', 'MP2','MP3','MP4','CT1','CT2']),
                Simulation(name='S3: Vessel Arrival & Turnaround',
                           df=turnaround,
                           invalid_cols={'service_time' : equal_zero},
                           continuous_cols=['service_time']),
                Simulation(name='S4: Container Move Simulation',
                           df=container,
                           invalid_cols={'teu_handled' : equal_zero,
                                        'move_duration' : equal_zero},
                           continuous_cols=['teu_handled', 'move_duration']),
                Simulation(name='S5: Crane & RTG Uptime & Downtime',
                           df=crane),
                Simulation(name='S6: Gate-Entry Traffic',
                           df=gate),
                Simulation(name='S7: Energy Consumption Profile',
                           df=energy),
                Simulation(name='S8: Maintenance Event Simulation',
                           df=maintenance)]

def new_page(title):
    '''
    Returns a figure that can be a new page of the pdf
    Parameters
    title: the desired title string of the new page
    Returns
    fig: matplotlib plt.figure() object
    '''
    # The fig is the container for all of the elements
    fig = plt.figure(figsize=(8,6))

    # Make a title displaying the title of this simulation
    fig.text(0.5, 0.95, title, ha='center', va='top', fontsize=16)

    return fig

with PdfPages('Data_Quality_Hazira_Report.pdf') as pdf:
    for sim in SIMULATIONS:
        fig = new_page(sim.name)

        # Count the percent of zero values (when zeros are invalid) for each of such columns
        percent_missing(sim, fig)
        pdf.savefig(fig)
        plt.close(fig) # Clears the plot of this figure

        fig = new_page(sim.name)
        invalid_col(sim, fig)
        pdf.savefig(fig)
        plt.close(fig)

        # Check for outliers in each column that we expect outliers
        for col in sim.continuous_cols:
            fig = new_page(sim.name)
            outlier_detection(sim, fig, col)
            pdf.savefig(fig)
            plt.close(fig)
