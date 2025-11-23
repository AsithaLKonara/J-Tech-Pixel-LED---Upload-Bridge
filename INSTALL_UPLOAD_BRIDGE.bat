@echo off
title J Tech Pixel Upload Bridge - Professional Installer
color 0A

REM Check for administrator privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Running with administrator privileges
) else (
    echo ❌ This installer requires administrator privileges
    echo.
    echo Please right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo.
echo  ██╗     ████████╗███████╗ ██████╗██╗  ██╗    ██████╗ ██████╗ ██╗██████╗  ██████╗ ███████╗
echo  ██║     ╚══██╔══╝██╔════╝██╔════╝██║  ██║    ██╔══██╗██╔══██╗██║██╔══██╗██╔════╝ ██╔════╝
echo  ██║        ██║   █████╗  ██║     ███████║    ██████╔╝██████╔╝██║██║  ██║██║  ███╗█████╗  
echo  ██║        ██║   ██╔══╝  ██║     ██╔══██║    ██╔══██╗██╔══██╗██║██║  ██║██║   ██║██╔══╝  
echo  ███████╗   ██║   ███████╗╚██████╗██║  ██║    ██║  ██║██║  ██║██║██████╔╝╚██████╔╝███████╗
echo  ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝  ╚═════╝ ╚══════╝
echo.
echo  ██╗     ██╗██████╗  ██████╗ ███████╗    ███████╗████████╗██╗   ██╗██████╗ ██╗   ██╗
echo  ██║     ██║██╔══██╗██╔════╝ ██╔════╝    ██╔════╝╚══██╔══╝██║   ██║██╔══██╗╚██╗ ██╔╝
echo  ██║     ██║██║  ██║██║  ███╗█████╗      █████╗     ██║   ██║   ██║██████╔╝ ╚████╔╝ 
echo  ██║     ██║██║  ██║██║   ██║██╔══╝      ██╔══╝     ██║   ██║   ██║██╔══██╗  ╚██╔╝  
echo  ███████╗██║██████╔╝╚██████╔╝███████╗    ███████╗   ██║   ╚██████╔╝██║  ██║   ██║   
echo  ╚══════╝╚═╝╚═════╝  ╚═════╝ ╚══════╝    ╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
echo.
echo ========================================
echo  J Tech Pixel Upload Bridge
echo  Professional GUI Installer
echo ========================================
echo.
echo  Universal LED Matrix Firmware Uploader
echo  Supports: ESP8266, ESP32, AVR, STM32, PIC, Nuvoton
echo.
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from: https://python.org
    echo Then run this installer again.
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if tkinter is available
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo ❌ tkinter is not available
    echo.
    echo Please install tkinter with your Python installation
    echo.
    pause
    exit /b 1
)

echo ✅ tkinter available
echo.

echo 🚀 Starting GUI installer...
echo.

REM Run the GUI installer
python create_gui_installer.py

echo.
echo Installer has completed.
pause











