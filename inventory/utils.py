"""Utility functions for inventory app."""
from django.db.models import Sum, F, DecimalField
from decimal import Decimal
from .models import Book, Category


def get_stock_status(quantity):
    """
    Determine stock status based on quantity.
    
    Returns:
        dict: Contains 'status' and 'badge_class' keys
    """
    if quantity == 0:
        return {
            'status': 'Out of Stock',
            'badge_class': 'danger',
            'icon': '❌'
        }
    elif quantity <= 10:
        return {
            'status': 'Low Stock',
            'badge_class': 'warning',
            'icon': '⚠️'
        }
    else:
        return {
            'status': 'In Stock',
            'badge_class': 'success',
            'icon': '✅'
        }


def get_dashboard_stats():
    """
    Get dashboard statistics.
    
    Returns:
        dict: Contains various dashboard statistics
    """
    total_books = Book.objects.count()
    total_categories = Category.objects.count()
    total_stock = Book.objects.aggregate(
        total=Sum('stock_quantity')
    )['total'] or 0
    low_stock_count = Book.objects.filter(stock_quantity__lte=10).count()
    
    # Calculate total inventory value
    total_value = Book.objects.aggregate(
        value=Sum(F('price') * F('stock_quantity'), output_field=DecimalField())
    )['value'] or Decimal('0.00')
    
    # Calculate average book price (total value / total books)
    average_book_price = Decimal('0.00')
    if total_books > 0:
        average_book_price = total_value / total_books
    
    return {
        'total_books': total_books,
        'total_categories': total_categories,
        'total_stock': total_stock,
        'low_stock_count': low_stock_count,
        'total_inventory_value': total_value,
        'average_book_price': average_book_price,
    }


def get_books_per_category():
    """
    Get count of books per category.
    
    Returns:
        QuerySet: Categories with annotated book count
    """
    from django.db.models import Count
    return Category.objects.annotate(
        book_count=Count('books')
    ).order_by('-book_count')


def get_low_stock_books(limit=5):
    """
    Get books with low stock.
    
    Args:
        limit: Maximum number of books to return
        
    Returns:
        QuerySet: Low stock books
    """
    return Book.objects.filter(
        stock_quantity__lte=10
    ).select_related('category').order_by('stock_quantity')[:limit]
