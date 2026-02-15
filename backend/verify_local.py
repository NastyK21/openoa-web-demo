from app.core import run_simulation
from pathlib import Path
import time
import sys
import os

# Add current directory to path so we can import app
sys.path.append(os.getcwd())
# Add backend to path too just in case
sys.path.append(os.path.join(os.getcwd(), 'backend'))

if __name__ == "__main__":
    # Mock path - ensure you adjust this to where you actually put the data
    # We are running from d:\Projects\subhag\OpenOA
    TEST_DATA_PATH = Path("backend/data/la_haute_borne")
    print(f"Running simulation on {TEST_DATA_PATH}...")
    start_time = time.time()
    try:
        results = run_simulation(TEST_DATA_PATH)
        end_time = time.time()
        print("Success!")
        print(f"Execution time: {end_time - start_time:.2f} seconds")
        print("Results:")
        for k, v in results.items():
            if k != "distribution":
                print(f"  {k}: {v}")
            else:
                print(f"  {k}: [List of {len(v)} items]")
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
