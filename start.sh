#!/bin/bash

# Futures-War Project Startup Script
# Usage: ./start.sh [backend|frontend|all|docker]

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Activate venv if it exists
if [ -f "$VENV_DIR/bin/activate" ]; then
    echo -e "${BLUE}Activating virtual environment...${NC}"
    source "$VENV_DIR/bin/activate"
fi

# Command
COMMAND=${1:-all}

case $COMMAND in
    backend)
        echo -e "${BLUE}🚀 Starting Futures-War Backend...${NC}"
        cd "$BACKEND_DIR"
        echo -e "${YELLOW}Backend API will be available at: http://localhost:8000${NC}"
        echo -e "${YELLOW}API Docs at: http://localhost:8000/docs${NC}"
        python main.py
        ;;

    frontend)
        echo -e "${BLUE}🎨 Starting Futures-War Frontend...${NC}"
        cd "$FRONTEND_DIR"
        echo -e "${YELLOW}Frontend will be available at: http://localhost:3000${NC}"
        # Using Python's built-in http server
        python -m http.server 3000 --directory .
        ;;

    test)
        echo -e "${BLUE}🧪 Running Tests...${NC}"
        cd "$BACKEND_DIR"
        python -m pytest test_api.py -v
        ;;

    all)
        echo -e "${BLUE}🎯 Starting Futures-War (Full Stack)...${NC}"
        echo -e "${YELLOW}This will start both backend and frontend${NC}"
        echo -e "${YELLOW}Backend API: http://localhost:8000${NC}"
        echo -e "${YELLOW}Frontend: http://localhost:3000${NC}"
        echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
        
        # Start backend in background
        cd "$BACKEND_DIR"
        python main.py &
        BACKEND_PID=$!
        
        # Give backend time to start
        sleep 3
        
        # Start frontend in background (from frontend directory)
        cd "$FRONTEND_DIR"
        python -m http.server 3000 --directory . &
        FRONTEND_PID=$!
        
        echo -e "${GREEN}✅ Both services started!${NC}"
        echo "Backend PID: $BACKEND_PID"
        echo "Frontend PID: $FRONTEND_PID"
        echo "Press Ctrl+C to stop all services..."
        
        # Wait for both processes
        wait
        ;;

    docker)
        echo -e "${BLUE}🐳 Starting with Docker Compose...${NC}"
        docker-compose up
        ;;

    stop)
        echo -e "${BLUE}Stopping services...${NC}"
        pkill -f "python main.py" || true
        pkill -f "http.server 3000" || true
        echo -e "${GREEN}✅ Services stopped${NC}"
        ;;

    *)
        echo "Usage: $0 {backend|frontend|test|all|docker|stop}"
        echo ""
        echo "Commands:"
        echo "  backend  - Start only the FastAPI backend"
        echo "  frontend - Start only the frontend (HTTP server)"
        echo "  test     - Run API tests"
        echo "  all      - Start both backend and frontend"
        echo "  docker   - Start with Docker Compose"
        echo "  stop     - Stop all running services"
        exit 1
        ;;
esac
