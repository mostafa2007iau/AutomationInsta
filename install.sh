#!/bin/bash

# --- Helper Functions ---
function check_sudo() {
    if [ "$EUID" -ne 0 ]; then
        echo "⚠️ This script requires superuser privileges to manage Docker and install files in system directories."
        echo "Please run with sudo:"
        echo "sudo $0"
        exit 1
    fi
}

function detect_docker_compose() {
    if docker compose &> /dev/null; then
        DOCKER_COMPOSE_CMD="docker compose"
    elif docker-compose &> /dev/null; then
        DOCKER_COMPOSE_CMD="docker-compose"
    else
        echo "❌ Neither 'docker compose' nor 'docker-compose' could be found."
        echo "Please install Docker and Docker Compose to continue."
        exit 1
    fi
    echo "✅ Found Docker Compose command: '$DOCKER_COMPOSE_CMD'"
}

# --- Main Script ---
check_sudo
detect_docker_compose

echo ""
echo "Welcome to the Instagram Automation Setup Script!"
echo "------------------------------------------------"

# --- Installation Directory ---
echo "Where would you like to install the application?"
select INSTALL_DIR_CHOICE in "/opt/instagram-automation" "/srv/instagram-automation" "Current Directory"; do
    case $INSTALL_DIR_CHOICE in
        "/opt/instagram-automation"|"/srv/instagram-automation")
            INSTALL_DIR=$INSTALL_DIR_CHOICE
            break
            ;;
        "Current Directory")
            INSTALL_DIR=$(pwd)
            break
            ;;
    esac
done

# If installing in a system directory, move files there
if [ "$INSTALL_DIR" != "$(pwd)" ]; then
    echo "Installing application to $INSTALL_DIR..."
    mkdir -p "$INSTALL_DIR"
    # Move all files except the script itself
    rsync -av --progress . "$INSTALL_DIR" --exclude "$(basename "$0")"
    cd "$INSTALL_DIR" || exit 1
fi

# --- Environment Configuration ---
if [ -f .env ]; then
    echo "An existing .env file was found."
    read -p "Do you want to overwrite it? (y/n) [n]: " overwrite
    if [[ ! "$overwrite" =~ ^[Yy]$ ]]; then
        echo "Keeping existing .env file. Skipping port configuration."
    else
        # Remove old file to proceed with config
        rm .env
    fi
fi

if [ ! -f .env ]; then
    echo "How would you like to configure the ports?"
    select mode in "Default (Frontend: 8080)" "Manual"; do
        case $mode in
            "Default (Frontend: 8080)")
                FRONTEND_PORT=8080
                break
                ;;
            "Manual")
                read -p "Enter the port for the Frontend (e.g., 8080): " FRONTEND_PORT
                while ! [[ "$FRONTEND_PORT" =~ ^[0-9]+$ ]] || [ "$FRONTEND_PORT" -lt 1024 ] || [ "$FRONTEND_PORT" -gt 65535 ]; do
                    echo "Invalid port. Please enter a number between 1024 and 65535."
                    read -p "Enter the port for the Frontend: " FRONTEND_PORT
                done
                break
                ;;
        esac
    done

    echo "Creating .env file with your configuration..."
    echo "FRONTEND_PORT=${FRONTEND_PORT}" > .env
    echo ".env file created successfully!"
fi

# --- Build and Run Docker Containers ---
echo ""
echo "🚀 Building and starting the application with Docker Compose..."
echo "This may take a few minutes for the first build."
$DOCKER_COMPOSE_CMD up --build -d

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Success! The application is now running."
    echo "------------------------------------------------"
    echo "You can access the frontend at:"
    echo "   http://<YOUR_SERVER_IP>:${FRONTEND_PORT}"
    echo ""
    echo "To view logs, run: '$DOCKER_COMPOSE_CMD logs -f'"
    echo "To stop the application, run: '$DOCKER_COMPOSE_CMD down'"
    echo "------------------------------------------------"
else
    echo "❌ An error occurred while starting the Docker containers."
    echo "Please check the output above for details."
    echo "You can try running '$DOCKER_COMPOSE_CMD up --build' manually to diagnose the issue."
fi

exit 0
