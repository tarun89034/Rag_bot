FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install all dependencies in one layer
COPY server/requirements.txt /app/server/requirements.txt
COPY client/requirements.txt /app/client/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/server/requirements.txt && \
    pip install --no-cache-dir -r /app/client/requirements.txt

# Copy source code and script
COPY server/ /app/server/
COPY client/ /app/client/
COPY start.sh /app/start.sh

# Make start.sh executable
RUN chmod +x /app/start.sh

# Create upload directory and set permissions
RUN mkdir -p /app/server/uploaded_pdfs && chmod -R 777 /app

# Expose ports (Streamlit and FastAPI)
EXPOSE 7860 8080

# Environment variables
ENV API_URL=http://127.0.0.1:8080
ENV PYTHONUNBUFFERED=1

# Run with sh explicitly to avoid shebang/permission issues
CMD ["sh", "/app/start.sh"]
