from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from .api import router

app = FastAPI(title="OpenOA Web API")

# CORS (Allow all for MVP ease)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Static Files (Frontend)
# We assume the frontend is built to /app/frontend/dist in Docker
# Or locally at ../../frontend/dist relative to this file?
# Let's make it robust based on common locations.

# In Docker: /app/frontend/dist
# Local: backend/../frontend/dist
frontend_dist = Path(__file__).parent.parent.parent / "frontend" / "dist"
if not frontend_dist.exists():
    # Fallback for Docker structure if different
    frontend_dist = Path("/app/frontend/dist")

if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

    @app.get("/")
    async def serve_index():
        return FileResponse(frontend_dist / "index.html")
    
    # Catch-all for SPA client-side routing (if we had it, but good practice)
    @app.get("/{full_path:path}")
    async def catch_all(full_path: str):
        # If it's a file that exists, serve it (e.g. implicitly served by mount if under assets, but for root files like favicon)
        possible_file = frontend_dist / full_path
        if possible_file.exists() and possible_file.is_file():
            return FileResponse(possible_file)
        # Otherwise return index.html
        return FileResponse(frontend_dist / "index.html")
else:
    print(f"WARNING: Frontend dist not found at {frontend_dist}. API only mode.")
