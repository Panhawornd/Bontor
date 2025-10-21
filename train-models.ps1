Write-Host "Starting ML Model Training..." -ForegroundColor Green
Write-Host ""

# Navigate to ML service directory
Set-Location "ml-service"

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Run training
Write-Host "Training models with current data..." -ForegroundColor Green
python train_models.py

Write-Host ""
Write-Host "Training completed!" -ForegroundColor Green
Write-Host "Check the models folder for the trained model files." -ForegroundColor Cyan
