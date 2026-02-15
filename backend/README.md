# OpenOA Web App (MVP)

A web-based demonstration of the [OpenOA](https://github.com/NREL/OpenOA) library, specifically showcasing the **Monte Carlo Annual Energy Production (AEP)** analysis.

This application provides a user-friendly interface to run complex wind plant operational analyses on the "La Haute Borne" dataset, estimating long-term energy production with uncertainty quantification.

## 🚀 Features

-   **Monte Carlo Simulation**: Runs 50 iterations of AEP analysis using OpenOA.
-   **Instant Results**: View Mean AEP, P50/P90 estimates, and uncertainty percentages.
-   **Visualization**: Interactive distribution chart of simulation results.
-   **Bundled Data**: Comes pre-packaged with the La Haute Borne dataset for immediate execution.
-   **Production Ready**: Containerized with Docker, ready for deployment on platforms like Render.

## 🛠️ Tech Stack

-   **Backend**: Python 3.10, FastAPI, OpenOA (pinned version), Pandas, Scikit-learn.
-   **Frontend**: React, Vite, Recharts.
-   **Containerization**: Docker (Multi-stage build).

## 🐳 Quick Start (Docker)

The easiest way to run the application is via Docker.

1.  **Build the Image**:
    ```bash
    docker build -t openoa-app .
    ```

2.  **Run the Container**:
    ```bash
    docker run -p 8000:8000 openoa-app
    ```

3.  **Access the App**:
    Open [http://localhost:8000](http://localhost:8000) in your browser.

## 💻 Local Development

If you want to run the backend and frontend separately for development:

### Backend

1.  Navigate to the `backend` directory (technically root for this repo structure).
2.  Install dependencies:
    ```bash
    pip install -r backend/requirements.txt
    pip install -e .  # Install OpenOA in editable mode
    ```
3.  Start the server:
    ```bash
    python -m uvicorn backend.app.main:app --reload --port 8000
    ```

### Frontend

1.  Navigate to `frontend`:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the dev server:
    ```bash
    npm run dev
    ```
4.  Open [http://localhost:5173](http://localhost:5173).

## 📂 Architecture

-   **`backend/app/core.py`**: Wraps OpenOA logic, handles data loading, and ensures thread-safe execution.
-   **`backend/app/api.py`**: FastAPI router defining the `/api/aep/run` endpoint.
-   **`backend/app/main.py`**: Entry point, serves API and static frontend files.
-   **`frontend/src/App.jsx`**: Single-page React UI logic.
-   **`Dockerfile`**: Defines the optimized build process.

## 🤝 Credits

-   **OpenOA**: Developed by the National Renewable Energy Laboratory (NREL).
-   **Dataset**: La Haute Borne wind farm data (Engie).

---
*Built for the OpenOA MVP Validation Project.*
