@echo off
title Stopping AI Health Assistant

echo Stopping all servers...
taskkill /FI "WINDOWTITLE eq FastAPI Backend" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq React Frontend" /F >nul 2>&1
taskkill /IM "node.exe" /F >nul 2>&1
taskkill /IM "python.exe" /F >nul 2>&1

echo All servers stopped!
pause