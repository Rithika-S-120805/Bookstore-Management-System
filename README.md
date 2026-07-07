# Bookstore Inventory Management System

A Django-based inventory management system for bookstores, featuring category management, book inventory tracking, stock level monitoring, and user authentication.

## Features

- **User Authentication**: Login/Register functionality
- **Category Management**: Create, read, update, delete book categories
- **Book Management**: Full CRUD operations for books with validation
- **Inventory Tracking**: Real-time stock level monitoring with color-coded status badges
- **Search & Filtering**: Search books by title, author, ISBN, or category
- **Dashboard Analytics**: View statistics about inventory including:
  - Total books and categories
  - Total stock available
  - Low stock alerts
  - Books per category breakdown
  - Total inventory value calculations
- **Responsive UI**: Bootstrap 5 responsive design with navbar and sidebar navigation
- **Stock Status Indicators**: Visual badges showing stock status (In Stock, Low Stock, Out of Stock)

## Technology Stack

- **Backend**: Django 5.0.1
- **Database**: SQLite
- **Frontend**: HTML, CSS, Bootstrap 5
- **ORM**: Django ORM
- **Authentication**: Django built-in auth system

## Project Structure

```
bookstore/                    # Django project folder
├── manage.py               # Django management script
├── db.sqlite3              # SQLite database (created after migration)
├── requirements.txt        # Python dependencies
├── bookstore/              # Main project configuration
│   ├── settings.py         # Project settings
│   ├── urls.py             # URL routing
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
└── inventory/              # Main Django app
    ├── models.py           # Database models
    ├── views.py            # View functions
    ├── forms.py            # Django forms
    ├── admin.py            # Django admin configuration
    ├── urls.py             # App URL routing
    ├── utils.py            # Utility functions
    ├── templates/          # HTML templates
    │   ├── base.html       # Base template with navbar/sidebar
    │   ├── dashboard.html  # Dashboard view
    │   ├── category_*.html # Category templates
    │   ├── book_*.html     # Book templates
    │   ├── inventory.html  # Inventory view
    │   ├── auth/           # Authentication templates
    │   └── includes/       # Reusable template components
    └── static/             # Static files
        └── css/
            └── style.css   # Custom styling
```

## Installation & Setup

### Step 1: Install Python and Virtual Environment

1. Ensure Python 3.8+ is installed
2. Navigate to the project directory

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create Database & Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser

```bash
python manage.py createsuperuser
# Follow the prompts to create admin account
```

### Step 6: Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Usage

### Accessing the Application

- **Dashboard**: http://localhost:8000/
- **Django Admin**: http://localhost:8000/admin/
- **Categories**: http://localhost:8000/categories/
- **Books**: http://localhost:8000/books/
- **Inventory**: http://localhost:8000/inventory/

### Default Admin Access

Login with the superuser credentials created in Step 5.

## Database Models

### Category Model
- `id`: Auto-generated primary key
- `name`: Unique category name (required)
- `description`: Category description
- `created_at`: Auto-generated timestamp

### Book Model
- `id`: Auto-generated primary key
- `title`: Book title (required)
- `author`: Author name (required)
- `isbn`: Unique ISBN (13 digits, required)
- `category`: Foreign key to Category (required)
- `price`: Book price (must be > 0)
- `stock_quantity`: Stock quantity (non-negative, defaults to 0)
- `publication_date`: Book publication date (required)
- `created_at`: Auto-generated timestamp
- `updated_at`: Auto-updated timestamp

## Features in Detail

### Stock Status Indicators
- **In Stock** (Green): Stock quantity > 10
- **Low Stock** (Yellow): Stock quantity ≤ 10
- **Out of Stock** (Red): Stock quantity = 0

### Search Functionality
Search books by:
- Title (case-insensitive)
- Author (case-insensitive)
- ISBN
- Category name

### Inventory Analytics
- Total books count
- Total categories count
- Total stock available
- Low stock books count
- Total inventory value (Price × Quantity)
- Books per category breakdown

### Dashboard Features
- Key metrics displayed as cards
- Navigation cards for quick access to main sections
- Analytics section showing:
  - Books per category
  - Low stock alert list
  - Total inventory metrics

## Admin Interface Features

- **Category Admin**:
  - List all categories
  - Search by name or description
  - Create, edit, delete categories
  
- **Book Admin**:
  - List all books with key information
  - Filter by category and date
  - Search by title, author, ISBN
  - Display inventory value
  - Create, edit, delete books

## Validation Rules

- **ISBN**: Must be exactly 13 digits, unique
- **Price**: Must be greater than 0
- **Stock Quantity**: Must be non-negative (≥ 0)
- **Category Name**: Must be unique
- **Author & Title**: Required fields

## Authentication

- Users must log in to access CRUD operations
- Registration available for new users
- Dashboard is accessible to all users (read-only for non-authenticated)
- Login required redirects to login page

## Development Tips

### Load Sample Data

```bash
python manage.py shell
```

Then in the Python shell:

```python
from inventory.models import Category, Book
from datetime import date
from decimal import Decimal

# Create categories
fiction = Category.objects.create(name="Fiction", description="Fiction books")
tech = Category.objects.create(name="Technology", description="Tech books")

# Create books
Book.objects.create(
    title="Django for Beginners",
    author="William Vincent",
    isbn="9781719628778",
    category=tech,
    price=Decimal("29.99"),
    stock_quantity=15,
    publication_date=date(2022, 1, 1)
)
```

### Reset Database

```bash
# Delete db.sqlite3
rm db.sqlite3
# Or on Windows:
del db.sqlite3

# Recreate database
python manage.py migrate
python manage.py createsuperuser
```

## Production Deployment

Before deploying to production:

1. Set `DEBUG = False` in `settings.py`
2. Add allowed hosts to `ALLOWED_HOSTS`
3. Use a production database (PostgreSQL recommended)
4. Set up proper SECRET_KEY management (use environment variables)
5. Collect static files: `python manage.py collectstatic`
6. Use a production server (Gunicorn, uWSGI)

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Errors
```bash
python manage.py migrate --run-syncdb
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear
```

### Permission Denied on Models
Ensure the superuser has appropriate permissions in Django admin.

## Future Enhancements

- [ ] Email notifications for low stock
- [ ] CSV/PDF export functionality
- [ ] Bulk import of books
- [ ] Advanced analytics with charts
- [ ] Multi-user role-based access
- [ ] Audit logs for inventory changes
- [ ] Barcode scanning integration
- [ ] REST API endpoints

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please refer to Django documentation:
- [Django Documentation](https://docs.djangoproject.com/)
- [Django Models](https://docs.djangoproject.com/en/5.0/topics/db/models/)
- [Django Admin](https://docs.djangoproject.com/en/5.0/ref/contrib/admin/)
