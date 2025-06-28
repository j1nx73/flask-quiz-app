#!/bin/bash

# Flask Quiz App Deployment Script
# This script helps you deploy the quiz app to different platforms

set -e

echo "🚀 Flask Quiz App Deployment Script"
echo "=================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install dependencies
install_dependencies() {
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed successfully!"
}

# Function to run locally
run_local() {
    echo "🏃 Starting local development server..."
    python app.py
}

# Function to run with Gunicorn
run_production() {
    echo "🏭 Starting production server with Gunicorn..."
    if ! command_exists gunicorn; then
        echo "❌ Gunicorn not found. Installing..."
        pip install gunicorn
    fi
    gunicorn -w 4 -b 0.0.0.0:5000 app:app
}

# Function to build and run Docker
run_docker() {
    echo "🐳 Building and running Docker container..."
    if ! command_exists docker; then
        echo "❌ Docker not found. Please install Docker first."
        exit 1
    fi
    docker build -t quiz-app .
    docker run -p 5000:5000 quiz-app
}

# Function to deploy to Heroku
deploy_heroku() {
    echo "☁️ Deploying to Heroku..."
    if ! command_exists heroku; then
        echo "❌ Heroku CLI not found. Please install Heroku CLI first."
        exit 1
    fi
    heroku create
    git add .
    git commit -m "Deploy to Heroku"
    git push heroku main
    heroku open
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  install     Install dependencies"
    echo "  local       Run local development server"
    echo "  production  Run production server with Gunicorn"
    echo "  docker      Build and run with Docker"
    echo "  heroku      Deploy to Heroku"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 install     # Install dependencies"
    echo "  $0 local       # Run locally"
    echo "  $0 production  # Run with Gunicorn"
    echo "  $0 docker      # Run with Docker"
    echo "  $0 heroku      # Deploy to Heroku"
}

# Main script logic
case "${1:-help}" in
    install)
        install_dependencies
        ;;
    local)
        install_dependencies
        run_local
        ;;
    production)
        install_dependencies
        run_production
        ;;
    docker)
        run_docker
        ;;
    heroku)
        deploy_heroku
        ;;
    help|*)
        show_help
        ;;
esac 