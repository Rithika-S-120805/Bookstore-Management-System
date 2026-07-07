@echo off
REM Batch setup script for Django Bookstore Project
REM This script sets up the Django project from scratch

setlocal enabledelayedexpansion
title Bookstore Inventory System - Setup

echo.
echo ================================
echo Bookstore Inventory System Setup
echo ================================
echo.

REM Check if manage.py exists
if not exist manage.py (
    echo ERROR: manage.py not found. Run this script from the project root.
    pause
    exit /b 1
)

REM Try to find Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo WARNING: Python not found in PATH
    echo Please ensure Python is installed and added to PATH
    echo You can download Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)
echo.

REM Activate virtual environment (Windows)
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated.
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install Django
echo Installing Django and dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed.
echo.

REM Run migrations
echo Creating database migrations...
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo ERROR: Failed to create migrations
    pause
    exit /b 1
)
echo Migrations created.
echo.

echo Applying migrations to database...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Failed to migrate database
    pause
    exit /b 1
)
echo Database migrated successfully.
echo.

REM Create superuser
echo.
echo Creating superuser (admin account)...
echo Please enter the following information:
python manage.py createsuperuser

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo Next steps:
echo 1. Start the development server:
echo    python manage.py runserver
echo.
echo 2. Open your browser to:
echo    http://localhost:8000
echo.
echo 3. Admin panel:
echo    http://localhost:8000/admin/
echo.
pause
