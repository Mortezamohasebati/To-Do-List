@echo off
chcp 65001 >nul 2>&1
title Task Manager

echo.
echo  ======================================
echo        Advanced Task Manager
echo  ======================================
echo.

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python is not installed or not in PATH.
    echo  Please download Python from https://www.python.org
    pause
    exit /b 1
)

echo  Checking libraries...

:: Check and install PyQt5
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo  [INSTALL] Installing PyQt5...
    pip install PyQt5 --quiet -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
    if errorlevel 1 (
        echo  [ERROR] PyQt5 installation failed.
        pause
        exit /b 1
    )
    echo  [OK] PyQt5 installed.
) else (
    echo  [OK] PyQt5 available.
)

:: Check and install jdatetime (Persian calendar)
python -c "import jdatetime" >nul 2>&1
if errorlevel 1 (
    echo  [INSTALL] Installing jdatetime (Persian calendar)...
    pip install jdatetime --quiet -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
    if errorlevel 1 (
        echo  [ERROR] jdatetime installation failed.
        pause
        exit /b 1
    )
    echo  [OK] jdatetime installed.
) else (
    echo  [OK] jdatetime available.
)

echo.
echo  Running application...
echo.

cd /d "%~dp0"
python main.py

if errorlevel 1 (
    echo.
    echo  [ERROR] Application closed with error.
    pause
)