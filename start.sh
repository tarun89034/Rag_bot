#!/bin/bash
set -e

echo "Starting FastAPI backend on port 8080..."
cd /app/server
uvicorn main:app --host 0.0.0.0 --port 8080 &

echo "Waiting for backend to start..."
sleep 5

echo "Starting Streamlit frontend on port 7860..."
cd /app/client
streamlit run app.py \
    --server.port 7860 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false
