# PowerShell setup script for Django Bookstore Project
# Run with: .\setup.ps1

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Bookstore Inventory System Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "manage.py")) {
    Write-Host "ERROR: manage.py not found. Please run this script from the project root directory." -ForegroundColor Red
    exit 1
}

# Check if Python is available
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonPath) {
    Write-Host "ERROR: Python not found in PATH" -ForegroundColor Red
    Write-Host "Please install Python and add it to PATH" -ForegroundColor Red
    exit 1
}
Write-Host "Found Python at: $pythonPath" -ForegroundColor Green

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host ""
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    & python -m venv venv
    Write-Host "Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "Virtual environment already exists." -ForegroundColor Gray
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "Virtual environment activated." -ForegroundColor Green

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
& python -m pip install --upgrade pip
Write-Host "pip upgraded." -ForegroundColor Green

# Install requirements
Write-Host ""
Write-Host "Installing Django and dependencies..." -ForegroundColor Yellow
& pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "Dependencies installed successfully." -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Run migrations
Write-Host ""
Write-Host "Creating database migrations..." -ForegroundColor Yellow
& python manage.py makemigrations
if ($LASTEXITCODE -eq 0) {
    Write-Host "Migrations created successfully." -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to create migrations" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Applying migrations to database..." -ForegroundColor Yellow
& python manage.py migrate
if ($LASTEXITCODE -eq 0) {
    Write-Host "Database migrated successfully." -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to migrate database" -ForegroundColor Red
    exit 1
}

# Create superuser
Write-Host ""
Write-Host "Create a superuser for Django admin" -ForegroundColor Yellow
& python manage.py createsuperuser
if ($LASTEXITCODE -eq 0) {
    Write-Host "Superuser created successfully." -ForegroundColor Green
} else {
    Write-Host "Warning: Could not create superuser automatically" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Run the development server:" -ForegroundColor White
Write-Host "   python manage.py runserver" -ForegroundColor Gray
Write-Host "2. Open your browser to http://localhost:8000" -ForegroundColor Gray
Write-Host "3. Admin panel: http://localhost:8000/admin/" -ForegroundColor Gray
Write-Host ""
