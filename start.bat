@echo off
title AI Health Assistant

echo ============================================
echo    AI Health Assistant - Starting Up...
echo ============================================
echo.

:: Activate virtual environment
call venv\Scripts\activate

:: Start FastAPI in a new window
echo [1/2] Starting FastAPI backend on port 8000...
start "FastAPI Backend" cmd /k "call venv\Scripts\activate && uvicorn backend.main:app --reload --port 8000"

:: Wait 3 seconds for backend to start
timeout /t 3 /nobreak > nul

:: Start React in a new window
echo [2/2] Starting React frontend on port 3000...
start "React Frontend" cmd /k "cd frontend && npm start"

echo.
echo ============================================
echo    Both servers are starting!
echo    Backend  --> http://localhost:8000
echo    Frontend --> http://localhost:3000
echo    API Docs --> http://localhost:8000/docs
echo ============================================
echo.
pause