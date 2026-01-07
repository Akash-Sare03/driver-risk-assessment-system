FROM python:3.9-slim

# Set working directory
WORKDIR /app

# System dependencies required by OpenCV, MediaPipe, PIL
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better Docker caching)
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Create process launcher (FastAPI + Streamlit)
RUN printf "import subprocess\n\
import time\n\
\n\
# Start FastAPI (internal service)\n\
fastapi = subprocess.Popen([\n\
    'uvicorn', 'backend.main:app',\n\
    '--host', '0.0.0.0', '--port', '8000'\n\
])\n\
\n\
# Wait for backend to be ready\n\
time.sleep(5)\n\
\n\
# Start Streamlit (public UI)\n\
streamlit = subprocess.Popen([\n\
    'streamlit', 'run', 'frontend/app.py',\n\
    '--server.port', '8501',\n\
    '--server.address', '0.0.0.0',\n\
    '--server.enableCORS', 'false'\n\
])\n\
\n\
fastapi.wait()\n\
streamlit.wait()\n" > run_both.py

# Hugging Face exposes only one port
EXPOSE 8501

# Start both services
CMD ["python", "run_both.py"]
