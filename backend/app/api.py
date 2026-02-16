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

import time
import logging
import traceback

# Setup logger
logger = logging.getLogger("openoa.api")

@router.post("/aep/run", response_model=AEPResult)
def trigger_aep_analysis():
    """
    Trigger a synchronous MonteCarloAEP analysis on the bundled dataset.
    Returns the JSON results directly. 
    Running with reduced iterations (5) for demo stability.
    """
    start_time = time.perf_counter()
    logger.info("Starting MonteCarloAEP analysis request...")
    print(f"[{start_time}] Analysis requested")

    if not DATA_PATH.exists():
        logger.error(f"Data directory missing: {DATA_PATH}")
        raise HTTPException(status_code=500, detail=f"Data directory not found at {DATA_PATH}")

    try:
        # Synchronous call
        logger.info(f"Calling run_simulation with data at {DATA_PATH}")
        result = run_simulation(DATA_PATH)
        
        duration = time.perf_counter() - start_time
        success_msg = f"Analysis completed successfully in {duration:.2f} seconds"
        logger.info(success_msg)
        print(success_msg)
        
        return result

    except Exception as e:
        duration = time.perf_counter() - start_time
        error_msg = f"Analysis failed after {duration:.2f} seconds: {e}"
        logger.error(error_msg)
        print(error_msg)
        traceback.print_exc() # Ensure full stack trace is visible in Render logs
        raise HTTPException(status_code=500, detail=str(e))
