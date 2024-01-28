@echo off
REM Description: Run tests

REM Set path to the virtual environment and activate the virtual environment
cd backend/venv/Scripts/
call activate.bat
cd ../../..

REM Set path to test folder
cd backend/tests


REM Run tests
pytest -v
cd ../..