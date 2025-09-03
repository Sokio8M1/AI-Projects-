REM For those viewing this script...This is a batch script to set up and run the voice assistant project.
@echo off
echo ==============================
echo   Voice Assistant Setup
echo ==============================

REM Check if reset flag was passed
if "%1"=="reset" (
    echo Reset mode: deleting old virtual environment...
    rmdir /s /q venv
)

REM Step 1: Create virtual environment if missing
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Step 2: Activate virtual environment
call venv\Scripts\activate

REM Step 3: Upgrade pip
python -m pip install --upgrade pip

REM Step 4: Install from requirements2.txt
if exist requirements2.txt (
    echo Installing dependencies from requirements2.txt...
    pip install -r requirements2.txt
) else (
    echo requirements2.txt not found! Please create it in this folder.
    pause
    exit /b
)

REM Step 5: Run assistant
echo Starting your assistant...
python assistant.py

pause

