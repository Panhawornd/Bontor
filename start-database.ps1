Write-Host "Starting Grade Analyzer Database..." -ForegroundColor Green
Write-Host ""

# Check if Docker Desktop is running
try {
    docker version | Out-Null
    Write-Host "Docker Desktop is running." -ForegroundColor Green
} catch {
    Write-Host "Docker Desktop is not running. Starting Docker Desktop..." -ForegroundColor Yellow
    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    Write-Host "Waiting for Docker Desktop to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 15
}

# Start the database containers
Write-Host "Starting PostgreSQL and Redis containers..." -ForegroundColor Green
docker-compose up -d

# Wait a moment for containers to start
Start-Sleep -Seconds 5

# Check if containers are running
Write-Host ""
Write-Host "Checking container status..." -ForegroundColor Green
docker ps --filter "name=grade_analyzer"

Write-Host ""
Write-Host "Database is ready! You can now start your Next.js application." -ForegroundColor Green
Write-Host "Run: cd grade-analyze && npm run dev" -ForegroundColor Cyan
