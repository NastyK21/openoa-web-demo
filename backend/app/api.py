from fastapi import APIRouter, HTTPException
from .core import run_simulation, DATA_PATH
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional
import os

router = APIRouter()

# DATA_PATH is now centrally managed in core.py
# ensuring consistency between verification and API layers

class AEPResult(BaseModel):
    status: str
    aep_GWh_mean: float
    aep_GWh_p50: float
    aep_GWh_p90: float
    aep_GWh_p10: float
    std_dev: float
    uncertainty_pct: float
    distribution: List[float]

@router.post("/aep/run", response_model=AEPResult)
def trigger_aep_analysis():
    """
    Trigger a synchronous MonteCarloAEP analysis on the bundled dataset.
    Returns the JSON results directly.
    """
    if not DATA_PATH.exists():
        raise HTTPException(status_code=500, detail=f"Data directory not found at {DATA_PATH}")

    try:
        # Synchronous call - verified to take ~2.8s
        result = run_simulation(DATA_PATH)
        return result
    except Exception as e:
        # Log error in valid prod setup
        print(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
