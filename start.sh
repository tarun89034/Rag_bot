#!/bin/bash
set -e

echo "===== Starting RagBot 2.0 ====="

# Start FastAPI backend
echo "Starting FastAPI backend on port 8080..."
cd /app/server
nohup uvicorn main:app --host 0.0.0.0 --port 8080 > /tmp/uvicorn.log 2>&1 &
BACKEND_PID=$!
echo "Backend started with PID: $BACKEND_PID"

# Wait for backend to be ready
echo "Waiting for backend to start..."
for i in {1..30}; do
    if curl -s http://localhost:8080/test > /dev/null 2>&1; then
        echo "Backend is ready!"
        break
    fi
    echo "Waiting... ($i/30)"
    sleep 2
done

# Check if backend started successfully
if ! curl -s http://localhost:8080/test > /dev/null 2>&1; then
    echo "ERROR: Backend failed to start!"
    cat /tmp/uvicorn.log
    exit 1
fi

# Start Streamlit frontend
echo "Starting Streamlit frontend on port 7860..."
cd /app/client
streamlit run app.py \
    --server.port 7860 \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false \
    --server.enableCORS true &
    
echo "===== RagBot 2.0 started successfully ====="
echo "Streamlit: http://localhost:7860"
echo "API: http://localhost:8080"

# Keep the container running
wait
