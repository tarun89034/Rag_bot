#!/bin/bash
set -e

echo "Starting RagBot 2.0..."

# Start FastAPI backend
echo "Starting FastAPI on port 8080..."
cd /app/server
python -m uvicorn main:app --host 0.0.0.0 --port 8080 &
BACKEND_PID=$!

# Wait for backend
echo "Waiting for backend..."
sleep 10

# Start Streamlit
echo "Starting Streamlit on port 7860..."
cd /app/client
python -m streamlit run app.py \
    --server.port 7860 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false &

# Keep container running
echo "All services started!"
tail -f /dev/null
