#!/bin/bash

echo "Welcome to the Instagram Automation Setup Script!"
echo "------------------------------------------------"

# Check if .env file already exists
if [ -f .env ]; then
    echo "An existing .env file was found."
    read -p "Do you want to overwrite it? (y/n): " overwrite
    if [[ "$overwrite" != "y" ]]; then
        echo "Setup cancelled. Please manually edit your .env file if needed."
        exit 0
    fi
fi

# Ask the user for port configuration mode
echo "How would you like to configure the ports?"
select mode in "Default (Backend: 8000, Frontend: 8080)" "Manual"; do
    case $mode in
        "Default (Backend: 8000, Frontend: 8080)")
            BACKEND_PORT=8000
            FRONTEND_PORT=8080
            break
            ;;
        "Manual")
            read -p "Enter the port for the Backend (e.g., 8000): " BACKEND_PORT
            # Basic validation
            while ! [[ "$BACKEND_PORT" =~ ^[0-9]+$ ]] || [ "$BACKEND_PORT" -lt 1024 ] || [ "$BACKEND_PORT" -gt 65535 ]; do
                echo "Invalid port. Please enter a number between 1024 and 65535."
                read -p "Enter the port for the Backend: " BACKEND_PORT
            done

            read -p "Enter the port for the Frontend (e.g., 8080): " FRONTEND_PORT
            while ! [[ "$FRONTEND_PORT" =~ ^[0-9]+$ ]] || [ "$FRONTEND_PORT" -lt 1024 ] || [ "$FRONTEND_PORT" -gt 65535 ]; do
                echo "Invalid port. Please enter a number between 1024 and 65535."
                read -p "Enter the port for the Frontend: " FRONTEND_PORT
            done
            break
            ;;
    esac
done

# Create the .env file
echo "Creating .env file with your configuration..."
cat > .env << EOL
# --- Instagram Automation Environment Variables ---

# Port mapping for the Backend service (FastAPI)
BACKEND_PORT=${BACKEND_PORT}

# Port mapping for the Frontend service (Nginx)
FRONTEND_PORT=${FRONTEND_PORT}
EOL

echo ".env file created successfully!"
echo ""
echo "--- Next Steps ---"
echo "1. Make sure you have Docker and Docker Compose installed."
echo "2. Run the application using the following command:"
echo "   docker-compose up --build"
echo ""
echo "3. Once running, you can access the application at:"
echo "   Frontend: http://localhost:${FRONTEND_PORT}"
echo "   Backend API Docs: http://localhost:${BACKEND_PORT}/docs"
echo ""
echo "✅ Persistence: Thanks to the 'restart: unless-stopped' policy, these services will automatically restart if the server reboots."
echo "------------------------------------------------"
exit 0
