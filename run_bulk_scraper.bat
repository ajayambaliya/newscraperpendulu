@echo off
echo ========================================
echo OFFLINE BULK QUIZ SCRAPER
echo ========================================
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Run the bulk scraper
python offline_bulk_scraper.py

echo.
echo ========================================
echo Press any key to exit...
pause >nul
