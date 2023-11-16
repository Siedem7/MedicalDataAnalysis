@echo off
REM Author: @mpHcl
REM Description: Reinstall the virtual environment and npm dependencies
REM This script is used to reinstall the virtual environment and npm dependencies. 
REM (Or to install them for the first time.)

echo Deleting existing python virtual environment...
rmdir /s /q backend\venv

echo Creating new virtual environment...
python -m venv backend\venv

if exist backend\venv\Scripts\activate.bat (
    echo Virtual environment created successfully.
    echo Installing dependencies...
    call backend\venv\Scripts\activate.bat
    pip install -r backend\requirements.txt
    echo Dependencies installed successfully.
    call backend\venv\Scripts\deactivate.bat
) else (
    echo Error creating virtual environment.
)

echo Deleting existing node modules...
rmdir /s /q frontend\node_modules

echo Instaling npm scripts...
cd frontend 
call npm install
cd ..