@echo off
title SimpleShare v2.0 - Enhanced File Transfer
color 0b

echo.
echo ========================================
echo    SimpleShare v2.0 - Enhanced Edition
echo ========================================
echo.
echo Checking system requirements...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Create necessary directories
echo Creating directories...
if not exist "static\uploads" mkdir "static\uploads"
if not exist "static\downloads" mkdir "static\downloads"
if not exist "temp" mkdir "temp"

REM Check system resources
echo Checking system resources...
for /f "tokens=2 delims==" %%a in ('wmic computersystem get TotalPhysicalMemory /value') do set "total_memory=%%a"
set /a "memory_gb=%total_memory:~0,-1%/1024/1024/1024"
echo Available memory: %memory_gb% GB

REM Get local IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set "local_ip=%%a"
    goto :found_ip
)
:found_ip
set "local_ip=%local_ip: =%"

echo.
echo ========================================
echo    System Information
echo ========================================
echo Local IP: %local_ip%
echo Port: 5000
echo Max File Size: 500MB
echo Authentication: Enabled (PIN: 1234)
echo Real-time Updates: Enabled
echo.
echo ========================================
echo    Starting SimpleShare Server...
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python app.py

echo.
echo Server stopped.
pause 