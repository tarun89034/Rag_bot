FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install server dependencies
COPY server/requirements.txt /app/server/requirements.txt
RUN pip install --no-cache-dir -r /app/server/requirements.txt

# Install client dependencies
COPY client/requirements.txt /app/client/requirements.txt
RUN pip install --no-cache-dir -r /app/client/requirements.txt

# Pre-download the sentence-transformers model (verbose for debugging)
RUN python -c "print('Downloading model...'); from sentence_transformers import SentenceTransformer; model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2'); print('Model downloaded successfully.')"

# Copy source code
COPY server/ /app/server/
COPY client/ /app/client/
COPY start.sh /app/start.sh

# Create upload directory
RUN mkdir -p /app/server/uploaded_pdfs

# Make start script executable
RUN chmod +x /app/start.sh

# Expose Streamlit port (public-facing for Hugging Face Spaces)
EXPOSE 7860

# Set environment variable for internal API communication
ENV API_URL=http://127.0.0.1:8080
ENV PYTHONUNBUFFERED=1

# Ensure permissions for the entire app directory (HF uses UID 1000)
RUN chmod -R 777 /app

CMD ["/app/start.sh"]
