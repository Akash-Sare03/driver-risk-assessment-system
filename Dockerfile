FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install multiprocess

COPY . .

# Create combined Python app
RUN echo 'import subprocess\n\
import time\n\
import sys\n\
\n\
# Start FastAPI\n\
fastapi_process = subprocess.Popen(["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"])\n\
\n\
# Wait for FastAPI to start\n\
time.sleep(5)\n\
\n\
# Start Streamlit\n\
streamlit_process = subprocess.Popen(["streamlit", "run", "frontend/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"])\n\
\n\
# Keep both running\n\
fastapi_process.wait()\n\
streamlit_process.wait()\n\
' > run_both.py

EXPOSE 8501

CMD ["python", "run_both.py"]