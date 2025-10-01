#!/bin/bash

# Polish Peaks Development Helper Script

echo "🏔️ Polish Peaks Development Environment"
echo "======================================"

start_backend() {
    echo "🐍 Starting FastAPI backend..."
    cd backend
    python3 -m fastapi dev main.py &
    BACKEND_PID=$!
    echo "Backend PID: $BACKEND_PID"
    cd ..
}

start_frontend() {
    echo "⚛️  Starting Next.js frontend..."
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    echo "Frontend PID: $FRONTEND_PID"
    cd ..
}

stop_services() {
    echo "🛑 Stopping all services..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "Backend stopped"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "Frontend stopped"
    fi
    exit 0
}

trap stop_services SIGINT SIGTERM

case "$1" in
    "backend")
        start_backend
        wait $BACKEND_PID
        ;;
    "frontend") 
        start_frontend
        wait $FRONTEND_PID
        ;;
    "both"|"")
        start_backend
        start_frontend
        echo ""
        echo "✅ Both services are starting!"
        echo "📱 Frontend: http://localhost:3000"
        echo "🔧 Backend API: http://localhost:8000"
        echo "📚 API Docs: http://localhost:8000/docs"
        echo ""
        echo "Press Ctrl+C to stop all services"
        wait
        ;;
    *)
        echo "Usage: $0 [backend|frontend|both]"
        echo "  backend  - Start only the FastAPI backend"
        echo "  frontend - Start only the Next.js frontend"
        echo "  both     - Start both services (default)"
        exit 1
        ;;
esac