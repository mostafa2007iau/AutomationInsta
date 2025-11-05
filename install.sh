#!/bin/bash

# --- Helper Functions ---
function check_sudo_for_docker() {
    if [ "$EUID" -ne 0 ]; then
        echo "⚠️ Docker installation requires superuser privileges."
        echo "Please run with sudo: sudo $0"
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
        echo "Please install Docker and Docker Compose to continue with this option."
        return 1
    fi
    echo "✅ Found Docker Compose command: '$DOCKER_COMPOSE_CMD'"
    return 0
}

function get_port() {
    local port_prompt=$1
    local default_port=$2
    local port
    read -p "$port_prompt (default: $default_port): " port
    port=${port:-$default_port}
    while ! [[ "$port" =~ ^[0-9]+$ ]] || [ "$port" -lt 1024 ] || [ "$port" -gt 65535 ]; do
        echo "Invalid port. Please enter a number between 1024 and 65535."
        read -p "$port_prompt (default: $default_port): " port
        port=${port:-$default_port}
    done
    echo $port
}

# --- Installation Logic ---

function install_docker() {
    check_sudo_for_docker
    if ! detect_docker_compose; then
        exit 1
    fi

    local FRONTEND_PORT=$(get_port "Enter the public-facing port for the Web UI" "8080")

    echo "Creating .env file with your configuration..."
    echo "FRONTEND_PORT=${FRONTEND_PORT}" > .env

    echo "🚀 Building and starting the application with Docker Compose..."
    $DOCKER_COMPOSE_CMD up --build -d

    if [ $? -eq 0 ]; then
        echo "✅ Success! The application is running via Docker."
        echo "Access the UI at: http://<YOUR_SERVER_IP>:${FRONTEND_PORT}"
    else
        echo "❌ Docker Compose failed. Please check the logs."
    fi
}

function install_venv() {
    if [ "$EUID" -eq 0 ]; then
        echo "⚠️ It's not recommended to run the venv installation as root. Please run without sudo."
        read -p "Are you sure you want to continue as root? (y/n) [n]: " confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            exit 0
        fi
    fi

    echo "Setting up Python virtual environment..."
    if ! python3 -m venv .venv; then
        echo "❌ Failed to create virtual environment. Is python3-venv installed?"
        exit 1
    fi

    source .venv/bin/activate
    echo "Installing dependencies from requirements.txt..."
    pip install -r backend/requirements.txt

    local BACKEND_PORT=$(get_port "Enter the port for the backend service" "8000")
    local FRONTEND_PORT=$(get_port "Enter the port for the frontend service" "8080")

    echo "Configuring systemd services..."
    local INSTALL_PATH=$(pwd)
    local USER=$(whoami)

    # --- Create backend service file ---
    sed -e "s|{{USER}}|$USER|g" \
        -e "s|{{INSTALL_PATH}}|$INSTALL_PATH|g" \
        -e "s|{{BACKEND_PORT}}|$BACKEND_PORT|g" \
        deployment/insta-backend.service > /tmp/insta-backend.service

    # --- Create frontend service file ---
    # A simple python server to serve static frontend files
    sed -e "s|{{USER}}|$USER|g" \
        -e "s|{{INSTALL_PATH}}|$INSTALL_PATH|g" \
        -e "s|{{FRONTEND_PORT}}|$FRONTEND_PORT|g" \
        deployment/insta-frontend.service > /tmp/insta-frontend.service

    echo "The script needs sudo privileges to install systemd services."
    sudo mv /tmp/insta-backend.service /etc/systemd/system/
    sudo mv /tmp/insta-frontend.service /etc/systemd/system/

    echo "Reloading systemd, enabling and starting services..."
    sudo systemctl daemon-reload
    sudo systemctl enable --now insta-backend.service
    sudo systemctl enable --now insta-frontend.service

    if sudo systemctl is-active --quiet insta-backend.service && sudo systemctl is-active --quiet insta-frontend.service; then
        echo "✅ Success! The application is running via systemd."
        echo "Access the UI at: http://<YOUR_SERVER_IP>:${FRONTEND_PORT}"
    else
        echo "❌ Services failed to start. Check status with:"
        echo "sudo systemctl status insta-backend.service"
        echo "sudo systemctl status insta-frontend.service"
    fi
}


# --- Main Script ---
echo "Welcome to the Instagram Automation Setup Script!"
echo "------------------------------------------------"
echo "Please choose your installation method:"
select INSTALL_METHOD in "Docker (Recommended)" "Python venv (Manual)"; do
    case $INSTALL_METHOD in
        "Docker (Recommended)")
            install_docker
            break
            ;;
        "Python venv (Manual)")
            install_venv
            break
            ;;
    esac
done

exit 0
