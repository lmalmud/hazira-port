'''
run_all.py
A single script to run all simulations followed by the metric scripts,
and then open relevant Excel files to automatically refresh data.

To make executable on Mac/Linux:
chmod +x run_all.py
./run_all.py
'''

import subprocess
import sys
import os

# 1. Simulation scripts (in order)
SIM_SCRIPTS = [
    "simulation_tasks/simulate_berth_hazira.py",
    "simulation_tasks/simulate_vessels_hazira.py",
    "simulation_tasks/simulate_containers_hazira.py",
    "simulation_tasks/simulate_cranes_hazira.py",
    "simulation_tasks/simulate_gate_hazira.py",
    "simulation_tasks/simulate_energy_hazira.py",
    "simulation_tasks/simulate_maintenance_hazira.py",
]

# 2. Metric‐aggregation scripts
METRIC_SCRIPTS = [
    "simulation_tasks/process_metrics_hazira.py",   # e.g. computes monthly KPIs
    "ai_scenario_simulation/apply_scenario_hazira.py",
    "ai_scenario_simulation/compute_savings_hazira.py"
]

# 3. Excel workbooks to open at the end
EXCEL_FILES = [
    "simulation_tasks/hazira_monthly_metrics.xlsx",
    "baseline_cost_model_inputs/Cost_Model_Hazira.xlsx",
    "ai_scenario_simulation/Cost_Savings_Summary.xlsx",
    "financial_projection_and_sensitivity/ROI_NPV_Payback_Hazira.xlsx",
    "financial_projection_and_sensitivity/Sensitivity_Analysis_Hazira.xlsx"
]

# ───────────────────────────────────────────────────────────────
def run_script(script_name):
    """Run a Python script in this same directory."""
    script_path = os.path.abspath(script_name)
    script_dir  = os.path.dirname(script_path)
    print(f"→ Running {script_name} in {script_dir}...")
    try:
        subprocess.run([sys.executable, script_path], 
                       cwd=script_dir, # Want to run in *this* folder
                       check=True)
    except subprocess.CalledProcessError as e:
        print(f"✗ Error running {script_name}: {e}")
        sys.exit(1)

def open_file(path):
    """Open a file with the default application (macOS 'open')."""
    print(f"→ Opening {path} ...")
    if sys.platform == "darwin":
        subprocess.run(["open", path])
    elif sys.platform.startswith("win"):
        subprocess.run(["start", "", path], shell=True)
    else:
        # Linux: try xdg-open
        subprocess.run(["xdg-open", path])

def main():
    cwd = os.getcwd()
    print(f"Working directory: {cwd}")

    # 1. Run all simulations
    for sim in SIM_SCRIPTS:
        run_script(sim)

    # 2. Run all metric scripts
    for metric in METRIC_SCRIPTS:
        run_script(metric)

    # 3. Open final Excel workbooks
    for xlsx in EXCEL_FILES:
        if not os.path.exists(xlsx):
            print(f"Warning: {xlsx} not found")
            continue
        open_file(xlsx)

    print("🎉 All done!")

if __name__ == "__main__":
    main()
