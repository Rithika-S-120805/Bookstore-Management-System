# Django Bookstore Project - Complete Setup Guide

## Project Status:Project Structure Created

All Django project files, app structure, templates, and models have been created. Now you need to:
1. Install Python (if not already installed)
2. Install Django and dependencies
3. Run migrations
4. Create a superuser
5. Start the development server

---

## Prerequisites

- **Python 3.8 or higher**
- **pip (Python package manager)**
- **Windows 10/11, macOS, or Linux**

---

## Installation Steps

### Step 1: Install Python

#### Option A: Standard Python Installation (Recommended)

1. Download Python from: https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check the box "Add Python to PATH"
4. Click "Install Now"
5. Wait for installation to complete

#### Option B: Microsoft Store (Alternative)

If you prefer, you can install from Microsoft Store, but you may need to:
1. Disable app execution aliases for Python
2. Or use the standard installation above instead

### Step 2: Verify Python Installation

Open Command Prompt (cmd.exe) or PowerShell and type:

```
python --version
```

You should see: `Python 3.x.x`

If not found, add Python to PATH manually or reinstall with the PATH option checked.

---

## Automated Setup (Recommended)

### Option A: Using Batch File (Windows)

1. Open File Explorer
2. Navigate to: `d:\bookstore_ptoject`
3. Double-click: `setup.bat`
4. Follow the prompts
5. When asked to create a superuser, enter:
   - Username: `admin`
   - Email: `admin@example.com`
   - Password: (create a strong password)
   - Confirm Password: (re-enter the same password)

### Option B: Using PowerShell Script (Windows)

1. Open PowerShell as Administrator
2. Navigate to project: `cd d:\bookstore_ptoject`
3. Allow script execution: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
4. Run: `.\setup.ps1`
5. Follow the prompts

---

## Manual Setup (If automated scripts don't work)

### Step 1: Create Virtual Environment

Open Command Prompt and type:

```bash
cd d:\bookstore_ptoject
python -m venv venv
```

### Step 2: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command prompt.

### Step 3: Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Django 5.0.1
- Pillow 10.1.0

### Step 5: Create Database Migrations

```bash
python manage.py makemigrations
```

Expected output:
```
Migrations for 'inventory':
  inventory/migrations/0001_initial.py
    - Create model Category
    - Create model Book
```

### Step 6: Apply Migrations

```bash
python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, inventory
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying inventory.0001_initial... OK
```

### Step 7: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

You'll be prompted for:
- **Username**: admin
- **Email address**: admin@example.com
- **Password**: (create a password)
- **Password (again)**: (confirm password)

Example:
```
Username: admin
Email address: admin@example.com
Password: 
Confirm password:
Superuser created successfully.
```

---

## Running the Application

### Start Development Server

With the virtual environment activated, type:

```bash
python manage.py runserver
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Access the Application

Open your web browser and go to:

1. **Dashboard**: http://localhost:8000/
2. **Books Page**: http://localhost:8000/books/
3. **Categories Page**: http://localhost:8000/categories/
4. **Inventory Page**: http://localhost:8000/inventory/
5. **Admin Panel**: http://localhost:8000/admin/

---

## First Time Usage

### 1. Log In to Admin Panel

1. Go to: http://localhost:8000/admin/
2. Login with your superuser credentials (admin / password)
3. You can now add categories and books through the admin interface

### 2. Create Sample Data (Admin Panel)

1. Click "Categories" → "Add Category"
2. Add your first category (e.g., "Fiction", "Technology")
3. Click "Books" → "Add Book"
4. Fill in the book details:
   - Title: "Python Programming"
   - Author: "Guido van Rossum"
   - ISBN: "1234567890123" (must be 13 digits)
   - Category: Select your category
   - Price: 29.99
   - Stock Quantity: 10
   - Publication Date: 2020-01-01
5. Click "Save"

### 3. Register User (Dashboard)

1. Go to http://localhost:8000/auth/register/
2. Fill in the registration form
3. Your account will be created and you'll be logged in
4. You can now add/edit/delete books from the main interface

---

## Troubleshooting

### "Python not found" or "command not recognized"

**Solution**: Python is not in your PATH. Either:
- Reinstall Python and check "Add Python to PATH"
- Or manually add Python to PATH in System Environment Variables

### Virtual Environment Not Activating

**Windows:**
```
If you get an error, try:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Then try activating again.
```

**Alternative:**
Use the batch file: Run `venv\Scripts\activate.bat` directly in Command Prompt

### "ModuleNotFoundError: No module named 'django'"

**Solution**: Make sure virtual environment is activated (you should see `(venv)` in your prompt)

Then install again:
```bash
pip install -r requirements.txt
```

### "Port 8000 already in use"

**Solution**: Use a different port:
```bash
python manage.py runserver 8001
```

Or find and kill the process using port 8000:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Database locked error

**Solution**: Delete the database and recreate it:
```bash
# Delete the database file
del db.sqlite3

# Recreate it
python manage.py migrate
python manage.py createsuperuser
```

---

## What's Already Set Up

✅ **Phase 1 - Project Setup Complete:**
- Django project structure created
- Inventory app initialized
- All models defined (Category, Book)
- Admin interface configured
- All forms created with validation
- All views and URL routing set up
- Templates created (all HTML files)
- CSS styling configured
- Authentication system ready
- Database migrations prepared

---

## Next Steps After Setup

1. Add some sample books in admin panel
2. Test the search functionality
3. Verify stock status badges appear correctly
4. Check the dashboard analytics
5. Test user registration and login
6. Explore all pages (Categories, Books, Inventory)

---

## Project Files Overview

```
d:\bookstore_ptoject\
├── manage.py                    # Django management script
├── requirements.txt             # Python packages to install
├── README.md                    # Project documentation
├── setup.bat / setup.ps1        # Automated setup scripts
├── .gitignore                   # Git ignore file
├── db.sqlite3                   # Database (created after migrate)
├── bookstore/                   # Main Django project
│   ├── settings.py             # Project settings ✅ Configured
│   ├── urls.py                 # URL routing ✅ Set up
│   ├── wsgi.py / asgi.py       # Deployment config
│   └── __init__.py
└── inventory/                   # Main Django app
    ├── models.py               # ✅ Category & Book models
    ├── views.py                # ✅ All view functions
    ├── forms.py                # ✅ Category & Book forms
    ├── admin.py                # ✅ Admin configuration
    ├── urls.py                 # ✅ URL routing
    ├── utils.py                # ✅ Utility functions
    ├── apps.py
    ├── migrations/             # Database migrations (auto-generated)
    │   ├── __init__.py
    │   └── 0001_initial.py     # Will be created by makemigrations
    ├── templates/              # ✅ All HTML templates
    │   ├── base.html           # Main layout template
    │   ├── dashboard.html      # Dashboard page
    │   ├── category_*.html     # Category pages
    │   ├── book_*.html         # Book pages
    │   ├── inventory.html      # Inventory page
    │   ├── auth/
    │   │   ├── login.html      # Login page
    │   │   └── register.html   # Registration page
    │   └── includes/           # Reusable components
    │       ├── navbar.html
    │       ├── sidebar.html
    │       ├── messages.html
    │       └── pagination.html
    ├── static/                 # ✅ Static files
    │   └── css/
    │       └── style.css       # Custom styling
    └── __init__.py
```

---

## Default Credentials (After Setup)

- **Admin Username**: admin
- **Admin Password**: (whatever you set during `createsuperuser`)
- **Dashboard URL**: http://localhost:8000/
- **Admin URL**: http://localhost:8000/admin/

---

## Need Help?

If you encounter issues:

1. Check the troubleshooting section above
2. Verify Python is installed: `python --version`
3. Verify virtual environment is activated: `(venv)` should show in terminal
4. Check that all files are in place: `ls` or `dir`
5. Review the README.md for more details

---

**Happy Managing Your Bookstore Inventory! 📚**
