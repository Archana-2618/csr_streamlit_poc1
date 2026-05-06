import subprocess
import sys
import time

def main():
    print("Starting FastAPI Backend...")
    # Start backend
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"],
    )
    
    time.sleep(2)  # Give backend a moment to start
    
    print("Starting Streamlit Frontend...")
    # Start frontend
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--server.port", "8502"]
    )
    
    try:
        # Keep the main process alive
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    main()
