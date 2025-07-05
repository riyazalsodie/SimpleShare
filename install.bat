@echo off
echo.
echo ========================================
echo    SimpleShare - One-Click Installer
echo ========================================
echo.
echo Credits: R ! Y 4 Z
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.7+ from https://python.org
    echo.
    pause
    exit /b 1
)

echo [INFO] Python found! Installing dependencies...
echo.

:: Install required packages
echo [INFO] Installing Flask and dependencies...
pip install flask flask-cors flask-socketio qrcode pillow psutil

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo [SUCCESS] All dependencies installed successfully!
echo.
echo [INFO] Creating necessary directories...
if not exist "static\uploads" mkdir "static\uploads"
if not exist "static\downloads" mkdir "static\downloads"
if not exist "temp" mkdir "temp"

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo To start SimpleShare, run: start.bat
echo.
echo Or manually run: python app.py
echo.
echo Credits: R ! Y 4 Z
echo.
pause 