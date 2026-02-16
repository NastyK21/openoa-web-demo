# Stage 1: Build Frontend
FROM node:18-alpine as frontend-build

WORKDIR /frontend

# Copy dependencies first for caching
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

# Copy source and build
COPY frontend/ ./
# Fix: Vite 7 compatible build or rely on downgraded Vite 5
RUN npm run build

# Stage 2: Backend Runtime
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies required for OpenOA/Shapely/Cartopy
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgeos-dev \
    && rm -rf /var/lib/apt/lists/*

# Install OpenOA (Library)
COPY pyproject.toml README.md ./
COPY openoa/ ./openoa/
RUN pip install .

# Install Backend Dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install -r backend/requirements.txt

# Copy Backend Code & Data
COPY backend/ ./backend/

# Copy Frontend Build from Stage 1
COPY --from=frontend-build /frontend/dist ./frontend/dist

# Environment Setup
ENV PYTHONPATH=/app
ENV PORT=8000

# Expose Port
EXPOSE 8000

# Start Application
CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

