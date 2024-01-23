@echo off
REM Description: Run tests


REM Set path to test folder
cd backend/tests


REM Run tests
pytest -v
cd ../..