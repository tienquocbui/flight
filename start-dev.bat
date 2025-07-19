@echo off
echo 🚀 Starting Air Traffic Control Development Environment...
echo.

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running! Please start Docker Desktop first.
    pause
    exit /b 1
)

echo ✅ Docker is running
echo.

REM Check if project exists
if not exist "docker-compose.dev.yml" (
    echo ❌ Project files not found! Please run this script from the project directory.
    pause
    exit /b 1
)

echo 📁 Project directory: %CD%
echo.

REM Build and start development environment
echo 🔨 Building development environment...
docker-compose -f docker-compose.dev.yml up --build

echo.
echo 🎉 Development environment started!
echo 📋 Available URLs:
echo    Backend API: http://localhost:8000
echo    Frontend: http://localhost:3000
echo    API Docs: http://localhost:8000/docs
echo.
echo 💡 To stop the environment, press Ctrl+C
pause 