@echo off
REM Author: @mpHcl
REM Description: Run the backend server
REM This script is used to run the backend server. It is called from run_all.bat.


REM Set path to the virtual environment and activate the virtual environment
cd backend/venv/Scripts/
call activate.bat
cd ../..

cd src
REM Run the backend server
python app.py