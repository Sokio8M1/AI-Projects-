@echo off
REM Auto-activate venv and run assistant.py (Windows)

if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate
)

python assistant.py
pause
