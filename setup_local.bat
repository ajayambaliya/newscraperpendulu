@echo off
REM Local Setup Script for Pendulumedu Quiz Scraper
REM This script helps you set up the project for local testing

echo ========================================
echo Pendulumedu Quiz Scraper - Local Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from python.org
    pause
    exit /b 1
)

echo [1/5] Python found
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [2/5] Creating virtual environment...
    python -m venv venv
    echo Virtual environment created successfully
) else (
    echo [2/5] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo [4/5] Installing dependencies...
pip install -r requirements.txt
echo.

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo [5/5] Creating .env file from template...
    copy .env.example .env
    echo.
    echo ========================================
    echo IMPORTANT: Configure your credentials!
    echo ========================================
    echo.
    echo Please edit the .env file and add your:
    echo   - LOGIN_EMAIL
    echo   - LOGIN_PASSWORD
    echo   - TELEGRAM_BOT_TOKEN
    echo   - TELEGRAM_CHANNEL
    echo.
    echo After configuring, run: python src/runner.py
    echo.
) else (
    echo [5/5] .env file already exists
    echo.
)

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your credentials
echo 2. Install Gujarati font (see LOCAL_TESTING_GUIDE.md)
echo 3. Run tests: python test_local_auth.py
echo 4. Run full system: python src/runner.py
echo.
echo For detailed testing instructions, see:
echo   LOCAL_TESTING_GUIDE.md
echo.

pause
