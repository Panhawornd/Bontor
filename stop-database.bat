@echo off
echo Stopping Grade Analyzer Database...
echo.

REM Stop the database containers
docker-compose down

echo.
echo Database containers stopped.
pause
