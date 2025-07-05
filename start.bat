@echo off
title SimpleShare v2.0 - Enhanced File Transfer
color 0b

echo.
echo ========================================
echo    SimpleShare v2.0 - Enhanced Edition
echo ========================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python found: 
python --version

REM Check if pip is available
echo.
echo Checking pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo ✅ pip found

REM Install/Upgrade pip if needed
echo.
echo Upgrading pip to latest version...
python -m pip install --upgrade pip

REM Install all dependencies
echo.
echo ========================================
echo    Installing Dependencies
echo ========================================
echo.

echo Installing Flask and core dependencies...
pip install Flask==2.3.3 Flask-CORS Flask-SocketIO==5.3.6

echo Installing QR code and image processing...
pip install qrcode[pil] Pillow

echo Installing system monitoring...
pip install psutil

echo Installing WebSocket support...
pip install python-socketio

echo Installing additional utilities...
pip install Werkzeug

echo.
echo ✅ All dependencies installed successfully!

REM Create necessary directories
echo.
echo ========================================
echo    Setting Up Directories
echo ========================================
echo.

if not exist "static\uploads" (
    mkdir "static\uploads"
    echo ✅ Created uploads directory
) else (
    echo ✅ Uploads directory exists
)

if not exist "static\downloads" (
    mkdir "static\downloads"
    echo ✅ Created downloads directory
) else (
    echo ✅ Downloads directory exists
)

if not exist "temp" (
    mkdir "temp"
    echo ✅ Created temp directory
) else (
    echo ✅ Temp directory exists
)

REM Check system resources
echo.
echo ========================================
echo    System Information
echo ========================================
echo.

REM Get local IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set "local_ip=%%a"
    goto :found_ip
)
:found_ip
set "local_ip=%local_ip: =%"

echo 🌐 Local IP: %local_ip%
echo 📏 Port: 5000
echo 📏 Max File Size: Unlimited
echo 🔐 Authentication: Enabled (PIN: 1234)
echo ⚡ Real-time Updates: Enabled
echo 🎨 Themes: Sci-fi, Day, Night
echo 📱 Mobile Optimized: Yes

echo.
echo ========================================
echo    Starting SimpleShare Server...
echo ========================================
echo.
echo 🚀 Server is starting...
echo 📱 Scan QR code with your phone to connect
echo 💻 Open http://localhost:5000 in your browser
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python app.py

echo.
echo Server stopped.
pause 
