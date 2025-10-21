@echo off
echo Starting Grade Analyzer Application...
echo.

REM Check if database is running
docker ps --filter "name=grade_analyzer_postgres" --format "table {{.Names}}\t{{.Status}}" | findstr "grade_analyzer_postgres" >nul
if %errorlevel% neq 0 (
    echo Database is not running. Starting database first...
    call start-database.bat
    echo.
)

REM Start the Next.js application
echo Starting Next.js development server...
cd grade-analyze
npm run dev
