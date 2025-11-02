#!/bin/bash

echo "Welcome to the venv Setup Script for the Instagram Automation App!"
echo "--------------------------------------------------------------------"

# Create a Python virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment in '.venv'..."
    python3 -m venv .venv
else
    echo "Virtual environment '.venv' already exists."
fi

# Activate the virtual environment and install dependencies
echo "Installing dependencies from backend/requirements.txt..."
source .venv/bin/activate
pip install -r backend/requirements.txt
deactivate

echo "Installation complete!"
echo ""

# --- Port Configuration ---
MANUAL_SETUP=false
read -p "Do you want to set ports manually? (y/n) [n]: " choice
case "$choice" in
  y|Y ) MANUAL_SETUP=true;;
  * ) MANUAL_SETUP=false;;
esac

if [ "$MANUAL_SETUP" = true ]; then
  read -p "Enter the port for the Backend (e.g., 8000): " BACKEND_PORT
  read -p "Enter the port for the Frontend (e.g., 8080): " FRONTEND_PORT
else
  BACKEND_PORT=8000
  FRONTEND_PORT=8080
fi

# --- Start Services ---
echo "Starting Backend service on port $BACKEND_PORT..."
nohup .venv/bin/uvicorn main:app --host 0.0.0.0 --port "$BACKEND_PORT" --app-dir backend > backend.log 2>&1 &
BACKEND_PID=$!

echo "Starting Frontend service on port $FRONTEND_PORT..."
nohup .venv/bin/python3 -m http.server "$FRONTEND_PORT" --directory frontend > frontend.log 2>&1 &
FRONTEND_PID=$!

echo "--------------------------------------------------------------------"
echo "✅ Services are running in the background!"
echo "   - Backend PID: $BACKEND_PID (Logs: backend.log)"
echo "   - Frontend PID: $FRONTEND_PID (Logs: frontend.log)"
echo ""
echo "You can access the application at: http://<YOUR_SERVER_IP>:$FRONTEND_PORT"
echo "--------------------------------------------------------------------"
