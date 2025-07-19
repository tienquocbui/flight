#!/bin/bash

echo "🚀 Starting Air Traffic Control Development Environment..."
echo

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running! Please start Docker Desktop first."
    exit 1
fi

echo "✅ Docker is running"
echo

# Check if project exists
if [ ! -f "docker-compose.dev.yml" ]; then
    echo "❌ Project files not found! Please run this script from the project directory."
    exit 1
fi

echo "📁 Project directory: $(pwd)"
echo

# Build and start development environment
echo "🔨 Building development environment..."
docker-compose -f docker-compose.dev.yml up --build

echo
echo "🎉 Development environment started!"
echo "📋 Available URLs:"
echo "   Backend API: http://localhost:8000"
echo "   Frontend: http://localhost:3000"
echo "   API Docs: http://localhost:8000/docs"
echo
echo "💡 To stop the environment, press Ctrl+C" 