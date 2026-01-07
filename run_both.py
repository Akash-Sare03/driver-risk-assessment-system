import subprocess
import time

# Start FastAPI (internal)
fastapi = subprocess.Popen([
    "uvicorn",
    "backend.main:app",
    "--host", "0.0.0.0",
    "--port", "8000"
])

# Give FastAPI time to boot
time.sleep(5)

# Start Streamlit (public)
streamlit = subprocess.Popen([
    "streamlit", "run", "frontend/app.py",
    "--server.port", "8501",
    "--server.address", "0.0.0.0",
    "--server.enableCORS", "false"
])

fastapi.wait()
streamlit.wait()
