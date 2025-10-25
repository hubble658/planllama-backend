@echo off
REM PlanLLaMA Backend Run Script for Windows

echo.
echo 🚀 PlanLLaMA Backend Setup ^& Run
echo ================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
if not exist "venv\installed" (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
    echo. > venv\installed
) else (
    echo ✅ Dependencies already installed
)

REM Check if .env exists
if not exist ".env" (
    echo ⚙️  Creating .env file from example...
    copy .env.example .env
    echo ⚠️  Please edit .env file with your configuration
)

REM Check if database exists
if not exist "planllama.db" (
    echo 🗄️  Initializing database with seed data...
    python init_db.py --seed
) else (
    echo ✅ Database already exists
)

echo.
echo 🎉 Setup complete! Starting server...
echo 📍 API will be available at: http://localhost:5000
echo 📖 API documentation: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the application
python app.py
