@echo off
REM Author: @mpHcl
REM Description: Run the backend and frontend servers
REM This script is used to run the servers used in the project. 


REM Run the backend server
start cmd /k run_frontend.bat

REM Run the frontend server
start cmd /k run_backend.bat