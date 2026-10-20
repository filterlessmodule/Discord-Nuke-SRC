@echo off
py --version >nul 2>&1 || (echo Python not found. Install from python.org && pause && exit /b)
py -m pip install -r requirements.txt
py main.py
pause