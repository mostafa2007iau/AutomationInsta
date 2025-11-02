#!/bin/bash

echo "Welcome to the venv Setup Script for the Instagram Automation Backend!"
echo "--------------------------------------------------------------------"

# Check if python3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: python3 is not installed. Please install Python 3 to continue."
    exit 1
fi

# 1. Create a Python virtual environment
echo "Creating Python virtual environment in './backend/.venv'..."
python3 -m venv backend/.venv

# 2. Activate the virtual environment and install dependencies
echo "Installing dependencies from backend/requirements.txt..."
# Note: Activating the venv in a script is tricky.
# It's better to call the python/pip from within the venv directly.
source backend/.venv/bin/activate
pip install -r backend/requirements.txt

echo "Installation complete!"
echo ""
echo "--- How to Run the Backend ---"
echo "1. Activate the virtual environment in your terminal:"
echo "   source backend/.venv/bin/activate"
echo ""
echo "2. Run the FastAPI application using uvicorn:"
echo "   uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir backend"
echo ""
echo "3. To run the frontend, you can use a simple HTTP server."
echo "   For example, with Python:"
echo "   python3 -m http.server 8080 --directory frontend"
echo ""
echo "4. Remember to update the API_BASE_URL in 'frontend/script.js' if you use different ports."
echo ""
echo "--- Making the Service Persistent ---"
echo "To ensure the application runs automatically after a server reboot, you should set it up as a systemd service."
echo "Template files and detailed instructions are available in the 'deployment' directory and the main README.md file."
echo "--------------------------------------------------------------------"

# The venv remains active in the current shell after sourcing,
# but the script will exit. This is expected.
exit 0
