import pandas as pd
import numpy as np
from pathlib import Path
from openoa.plant import PlantData
from openoa.analysis.aep import MonteCarloAEP
from openoa.utils import filters, unit_conversion as un

# Robust path resolution
# core.py is in backend/app/
# we want backend/data/la_haute_borne
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "la_haute_borne"

# Helper cleaning function (Simplified from project_ENGIE.py)
def clean_scada_data(scada_df):
    # Standardize time
    scada_df["Date_time"] = pd.to_datetime(scada_df["Date_time"], utc=True).dt.tz_localize(None)
    # Remove duplicates
    scada_df = scada_df.drop_duplicates(subset=["Date_time", "Wind_turbine_name"], keep="first")
    # Temp range filter
    scada_df = scada_df[(scada_df["Ot_avg"] >= -15.0) & (scada_df["Ot_avg"] <= 45.0)]
    # Convert pitch (simple modulo)
    scada_df.loc[:, "Ba_avg"] = scada_df["Ba_avg"] % 360
    # Calculate energy
    scada_df["energy_kwh"] = un.convert_power_to_energy(scada_df.P_avg * 1000, "10min") / 1000
    return scada_df

def prepare_plant_data(data_path: Path) -> PlantData:
    """
    Manually constructs PlantData from CSVs with necessary pre-cleaning.
    """
    # 1. Load & Clean SCADA
    scada_path = data_path / "la-haute-borne-data-2014-2015.csv"
    if not scada_path.exists():
         # Fallback to checking if it's zipped or named differently? 
         # The directory list showed "la-haute-borne-data-2014-2015.csv"
         pass

    scada_raw = pd.read_csv(scada_path)
    scada_clean = clean_scada_data(scada_raw)

    # 2. Load other CSVs (assuming they are pre-formatted/clean-ish from the repo example)
    meter_df = pd.read_csv(data_path / "plant_data.csv")
    meter_df["time"] = pd.to_datetime(meter_df["time_utc"]).dt.tz_localize(None)
    
    # Split meter/curtail (based on example logic)
    curtail_df = meter_df.copy()
    meter_df = meter_df.drop(["time_utc", "availability_kwh", "curtailment_kwh"], axis=1)
    curtail_df = curtail_df.drop(["time_utc"], axis=1)

    # Reanalysis
    era5 = pd.read_csv(data_path / "era5_wind_la_haute_borne.csv")
    merra2 = pd.read_csv(data_path / "merra2_la_haute_borne.csv")
    
    # Simple formatting for reanalysis (essential columns only)
    for df in [era5, merra2]:
        if "datetime" in df.columns:
             df["datetime"] = pd.to_datetime(df["datetime"], utc=True).dt.tz_localize(None)

    asset_df = pd.read_csv(data_path / "la-haute-borne_asset_table.csv")
    asset_df["type"] = "turbine"

    # 3. Construct PlantData
    # metadata.yml is required by PlantData validation
    plant = PlantData(
        analysis_type="MonteCarloAEP",
        metadata=data_path / "plant_meta.yml", # Point to file provided in bundled data
        scada=scada_clean,
        meter=meter_df,
        curtail=curtail_df,
        asset=asset_df,
        reanalysis={"era5": era5, "merra2": merra2}
    )
    return plant

def run_simulation(data_path: str):
    path = Path(data_path)
    if not path.exists():
        raise FileNotFoundError(f"Data not found at {path}")

    # Prepare
    project = prepare_plant_data(path)
    
    # Analysis
    # Reduced iterations for MVP speed (default is often 100-200)
    pa = MonteCarloAEP(project, reanalysis_products=['era5', 'merra2'])
    pa.run(num_sim=50) 
    
    # Result Extraction
    # pa.results is a DataFrame with simulation results
    aep_dist = pa.results['aep_GWh'] # Series
    
    stats = {
        "status": "success",
        "aep_GWh_mean": float(aep_dist.mean()),
        "aep_GWh_p50": float(aep_dist.median()),
        "aep_GWh_p90": float(aep_dist.quantile(0.10)),
        "aep_GWh_p10": float(aep_dist.quantile(0.90)),
        "std_dev": float(aep_dist.std()),
        "uncertainty_pct": float(aep_dist.std() / aep_dist.mean() * 100),
        "distribution": aep_dist.tolist()
    }
    return stats
