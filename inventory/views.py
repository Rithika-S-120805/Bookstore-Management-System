from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q, Count, Sum, F, DecimalField, DecimalField as DecimalFieldType
from decimal import Decimal
from django.views.decorators.http import require_http_methods
from django.utils import timezone

from .decorators import admin_required
from .models import Category, Book, Borrow
from .forms import CategoryForm, BookForm, BorrowIssueForm
from .utils import get_stock_status, get_dashboard_stats, get_books_per_category, get_low_stock_books


# Landing Page Views
def landing(request):
    """Display landing page with login/signup options."""
    return render(request, 'landing.html')


# Dashboard Views
@login_required(login_url='login')
def dashboard(request):
    """Display dashboard with key statistics."""
    if request.user.is_staff:
        stats = {
            'total_books': Book.objects.count(),
            'available_books': Book.objects.aggregate(total=Sum('stock_quantity'))['total'] or 0,
            'borrowed_books': Borrow.objects.active().count(),
            'returned_books': Borrow.objects.returned().count(),
            'overdue_books': Borrow.objects.overdue().count(),
            'total_users': User.objects.count(),
            'recent_activity': Borrow.objects.select_related('book', 'user').order_by('-updated_at', '-created_at')[:10],
        }
        context = {
            'is_admin_dashboard': True,
            'stats': stats,
            'books_per_category': get_books_per_category(),
            'low_stock_books': get_low_stock_books(limit=5),
            'issue_form': BorrowIssueForm(),
        }
    else:
        today = timezone.localdate()
        user_borrows = Borrow.objects.filter(user=request.user).select_related('book', 'book__category').order_by('-borrow_date', '-created_at')
        active_borrows = user_borrows.filter(status=Borrow.Status.BORROWED, return_date__isnull=True)
        returned_borrows = user_borrows.filter(status=Borrow.Status.RETURNED)
        due_borrows = active_borrows.filter(due_date__gte=today)
        overdue_borrows = user_borrows.filter(status=Borrow.Status.BORROWED, return_date__isnull=True, due_date__lt=today)

        context = {
            'is_admin_dashboard': False,
            'stats': {
                'currently_borrowed': active_borrows.count(),
                'returned_books': returned_borrows.count(),
                'due_books': due_borrows.count(),
                'overdue_books': overdue_borrows.count(),
            },
            'current_borrows': active_borrows,
            'returned_borrows': returned_borrows,
            'due_borrows': due_borrows,
            'overdue_borrows': overdue_borrows,
            'borrow_history': user_borrows,
        }
    return render(request, 'dashboard.html', context)


# Category Views
@admin_required
def category_list(request):
    """Display list of all categories with pagination and search."""
    queryset = Category.objects.all()
    search_query = request.GET.get('search', '')
    
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page', 1)
    categories = paginator.get_page(page_number)
    
    context = {
        'categories': categories,
        'search_query': search_query,
    }
    return render(request, 'category_list.html', context)


@admin_required
def category_detail(request, pk):
    """Display single category with its books."""
    category = get_object_or_404(Category, pk=pk)
    books = category.books.all().order_by('-created_at')
    
    paginator = Paginator(books, 20)
    page_number = request.GET.get('page', 1)
    books = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'books': books,
    }
    return render(request, 'category_detail.html', context)


@admin_required
def category_create(request):
    """Create a new category."""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category "{form.cleaned_data["name"]}" created successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    context = {'form': form, 'title': 'Add Category'}
    return render(request, 'category_form.html', context)


@admin_required
def category_edit(request, pk):
    """Edit an existing category."""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category "{form.cleaned_data["name"]}" updated successfully!')
            return redirect('category_detail', pk=category.pk)
    else:
        form = CategoryForm(instance=category)
    
    context = {'form': form, 'category': category, 'title': 'Edit Category'}
    return render(request, 'category_form.html', context)


@admin_required
@require_http_methods(["GET", "POST"])
def category_delete(request, pk):
    """Delete a category."""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('category_list')
    
    context = {'category': category}
    return render(request, 'category_confirm_delete.html', context)


# Book Views
@admin_required
def book_list(request):
    """Display list of books with pagination, search, filtering, and sorting."""
    queryset = Book.objects.select_related('category').all()
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    stock_status_filter = request.GET.get('stock_status', '')
    sort_by = request.GET.get('sort', '-created_at')
    
    # Search
    if search_query:
        queryset = queryset.search(search_query)
    
    # Category filter
    if category_filter:
        queryset = queryset.filter(category_id=category_filter)
    
    # Stock status filter
    if stock_status_filter == 'in_stock':
        queryset = queryset.in_stock()
    elif stock_status_filter == 'low_stock':
        queryset = queryset.low_stock()
    elif stock_status_filter == 'out_of_stock':
        queryset = queryset.out_of_stock()
    
    # Sorting
    allowed_sorts = [
        'title', '-title',
        'author', '-author',
        'price', '-price',
        'stock_quantity', '-stock_quantity',
        'created_at', '-created_at'
    ]
    if sort_by in allowed_sorts:
        queryset = queryset.order_by(sort_by)
    else:
        queryset = queryset.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page', 1)
    books = paginator.get_page(page_number)
    
    # Get all categories for filter dropdown
    categories = Category.objects.all().order_by('name')
    
    context = {
        'books': books,
        'search_query': search_query,
        'category_filter': category_filter,
        'stock_status_filter': stock_status_filter,
        'sort_by': sort_by,
        'categories': categories,
    }
    return render(request, 'book_list.html', context)


@admin_required
def book_detail(request, pk):
    """Display single book details."""
    book = get_object_or_404(Book, pk=pk)
    stock_status = get_stock_status(book.stock_quantity)
    
    context = {
        'book': book,
        'stock_status': stock_status,
    }
    return render(request, 'book_detail.html', context)


@admin_required
def book_create(request):
    """Create a new book."""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('book_list')
    else:
        form = BookForm()
    
    context = {'form': form, 'title': 'Add Book'}
    return render(request, 'book_form.html', context)


@admin_required
def book_edit(request, pk):
    """Edit an existing book."""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    context = {'form': form, 'book': book, 'title': 'Edit Book'}
    return render(request, 'book_form.html', context)


@admin_required
@require_http_methods(["GET", "POST"])
def book_delete(request, pk):
    """Delete a book."""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('book_list')
    
    context = {'book': book}
    return render(request, 'book_confirm_delete.html', context)


# Inventory Views
@admin_required
def inventory(request):
    """Display inventory management page with stock levels and values."""
    queryset = Book.objects.select_related('category').all()
    search_query = request.GET.get('search', '')
    stock_status_filter = request.GET.get('stock_status', '')
    sort_by = request.GET.get('sort', 'title')
    
    # Search
    if search_query:
        queryset = queryset.search(search_query)
    
    # Stock status filter
    if stock_status_filter == 'in_stock':
        queryset = queryset.in_stock()
    elif stock_status_filter == 'low_stock':
        queryset = queryset.low_stock()
    elif stock_status_filter == 'out_of_stock':
        queryset = queryset.out_of_stock()
    
    # Sorting
    allowed_sorts = ['title', 'author', 'stock_quantity', 'price', 'category__name']
    if sort_by not in allowed_sorts:
        sort_by = 'title'
    queryset = queryset.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page', 1)
    books = paginator.get_page(page_number)
    
    # Get statistics
    stats = {
        'total_books': Book.objects.count(),
        'total_value': Book.objects.aggregate(
            value=Sum(F('price') * F('stock_quantity'), output_field=DecimalField())
        )['value'] or Decimal('0.00'),
        'total_stock': Book.objects.aggregate(total=Sum('stock_quantity'))['total'] or 0,
        'low_stock_count': Book.objects.filter(stock_quantity__lte=10).count(),
        'out_of_stock_count': Book.objects.filter(stock_quantity=0).count(),
    }
    
    # Add stock status info to each book
    for book in books:
        book.stock_info = get_stock_status(book.stock_quantity)
    
    context = {
        'books': books,
        'stats': stats,
        'search_query': search_query,
        'stock_status_filter': stock_status_filter,
        'sort_by': sort_by,
    }
    return render(request, 'inventory.html', context)


# Auth Views
def register(request):
    """Register a new user."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validation
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
        elif password != password_confirm:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_staff = False
            user.is_superuser = False
            user.save(update_fields=['is_staff', 'is_superuser'])
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    
    return render(request, 'auth/register.html')


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def logout_view(request):
    """Handle user logout with confirmation."""
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('landing')
    
    # GET request - show confirmation page
    return render(request, 'auth/logout_confirm.html')


@admin_required
@require_http_methods(["GET", "POST"])
def issue_book(request):
    """Issue a book to a user with atomic stock handling."""
    if request.method != 'POST':
        return redirect('dashboard')

    form = BorrowIssueForm(request.POST)
    if not form.is_valid():
        for error_messages in form.errors.values():
            for error in error_messages:
                messages.error(request, error)
        return redirect('dashboard')

    selected_user = form.cleaned_data['user']
    selected_book = form.cleaned_data['book']
    due_date = form.cleaned_data['due_date']

    with transaction.atomic():
        user = User.objects.select_for_update().filter(pk=selected_user.pk).first()
        book = Book.objects.select_for_update().filter(pk=selected_book.pk).first()

        if user is None:
            messages.error(request, 'Selected user does not exist.')
            return redirect('dashboard')
        if book is None:
            messages.error(request, 'Selected book does not exist.')
            return redirect('dashboard')
        if book.stock_quantity <= 0:
            messages.error(request, 'Book currently unavailable.')
            return redirect('dashboard')
        if Borrow.objects.filter(user=user, book=book, status=Borrow.Status.BORROWED, return_date__isnull=True).exists():
            messages.error(request, 'This user already has an active borrow for this book.')
            return redirect('dashboard')

        Borrow.objects.create(
            user=user,
            book=book,
            borrow_date=timezone.localdate(),
            due_date=due_date,
            status=Borrow.Status.BORROWED,
        )
        book.stock_quantity -= 1
        book.save(update_fields=['stock_quantity'])

    messages.success(request, f'Book "{book.title}" issued to {user.username} successfully.')
    return redirect('dashboard')


@admin_required
@require_http_methods(["POST"])
def return_book(request, pk):
    """Mark a borrowed book as returned and calculate any overdue fine."""
    with transaction.atomic():
        borrow = Borrow.objects.select_for_update().select_related('book', 'user').filter(pk=pk).first()
        if borrow is None:
            messages.error(request, 'Borrow record not found.')
            return redirect('dashboard')
        if borrow.status == Borrow.Status.RETURNED or borrow.return_date is not None:
            messages.error(request, 'This book has already been returned.')
            return redirect('dashboard')

        return_date = timezone.localdate()
        fine_amount = Decimal('0.00')
        if return_date > borrow.due_date:
            days_late = (return_date - borrow.due_date).days
            fine_rate = Decimal(str(getattr(settings, 'OVERDUE_FINE_PER_DAY', '10.00')))
            fine_amount = Decimal(days_late) * fine_rate

        borrow.return_date = return_date
        borrow.status = Borrow.Status.RETURNED
        borrow.fine = fine_amount
        borrow.save(update_fields=['return_date', 'status', 'fine', 'updated_at'])

        if borrow.book_id:
            book = Book.objects.select_for_update().filter(pk=borrow.book_id).first()
            if book is not None:
                book.stock_quantity += 1
                book.save(update_fields=['stock_quantity'])

    messages.success(request, 'Book returned successfully.')
    return redirect('dashboard')
