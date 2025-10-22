@echo off
ECHO Starting NAC Server (app.py)...
start "NAC Server" cmd /k python app.py

ECHO Starting NAC Monitor (monitor.py)...
REM Updated the path below to point to the correct subfolder
start "NAC Monitor" cmd /k python network_monitor/monitor.py