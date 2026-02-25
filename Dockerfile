FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy and install server dependencies first (caching)
COPY server/requirements.txt /app/server/requirements.txt
RUN pip install --no-cache-dir -r /app/server/requirements.txt || echo "Server deps install attempted"

# Copy and install client dependencies
COPY client/requirements.txt /app/client/requirements.txt
RUN pip install --no-cache-dir -r /app/client/requirements.txt || echo "Client deps install attempted"

# Copy source code
COPY server/ /app/server/
COPY client/ /app/client/
COPY start.sh /app/start.sh
COPY .streamlit /app/.streamlit

# Make start.sh executable
RUN chmod +x /app/start.sh

# Create upload directory
RUN mkdir -p /app/server/uploaded_pdfs

# Expose ports
EXPOSE 7860 8080

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV API_URL=http://localhost:8080

CMD ["sh", "/app/start.sh"]
