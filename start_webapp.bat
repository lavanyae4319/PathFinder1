@echo off
echo ========================================
echo  Resume Analyzer and Job Predictor - Web Application
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found!
    echo Please run: python -m venv .venv
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Check if models exist
if not exist "models\job_matcher_model.pkl" (
    echo.
    echo WARNING: ML models not found!
    echo Please run the following notebooks first:
    echo   1. data_cleaning.ipynb
    echo   2. model_training.ipynb
    echo.
    pause
)

REM Check if .env exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please create .env file with your API keys
    echo See .env.example for template
    echo.
    pause
)

echo.
echo Starting Flask web application...
echo.
echo Access the application at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

python app.py

pause
