@echo off
echo ========================================
echo OFFLINE BULK QUIZ SCRAPER
echo ========================================
echo.

REM Check if virtual environment exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo No virtual environment found, using system Python
)

echo.
echo Checking Playwright installation...
python -c "from playwright.sync_api import sync_playwright; print('✓ Playwright is installed')" 2>nul
if errorlevel 1 (
    echo ✗ Playwright not found!
    echo.
    echo Installing Playwright...
    pip install playwright
    python -m playwright install chromium
)

echo.
echo Starting bulk scraper...
echo.

REM Run the bulk scraper
python offline_bulk_scraper.py

echo.
echo ========================================
echo Press any key to exit...
pause >nul
