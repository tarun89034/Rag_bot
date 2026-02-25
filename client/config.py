import os
# For local dev: defaults to localhost:8000
# For deployment: set API_URL as environment variable (e.g., http://127.0.0.1:8080)
API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")
