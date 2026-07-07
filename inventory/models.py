from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, DecimalValidator
from decimal import Decimal
from django.utils import timezone


class Category(models.Model):
    """Category model for organizing books."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class BookQuerySet(models.QuerySet):
    """Custom QuerySet for Book model."""
    def search(self, query):
        """Search books by title, author, ISBN, or category name."""
        return self.filter(
            models.Q(title__icontains=query) |
            models.Q(author__icontains=query) |
            models.Q(isbn__icontains=query) |
            models.Q(category__name__icontains=query)
        )

    def low_stock(self):
        """Filter books with low stock (<=10)."""
        return self.filter(stock_quantity__lte=10)

    def out_of_stock(self):
        """Filter books that are out of stock."""
        return self.filter(stock_quantity=0)

    def in_stock(self):
        """Filter books that are in stock (>10)."""
        return self.filter(stock_quantity__gt=10)


class BookManager(models.Manager):
    """Custom manager for Book model."""
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)

    def search(self, query):
        """Search books by multiple fields."""
        return self.get_queryset().search(query)

    def low_stock(self):
        """Get books with low stock."""
        return self.get_queryset().low_stock()

    def out_of_stock(self):
        """Get books out of stock."""
        return self.get_queryset().out_of_stock()

    def in_stock(self):
        """Get books in stock."""
        return self.get_queryset().in_stock()


class BorrowQuerySet(models.QuerySet):
    """Custom QuerySet for Borrow model."""

    def active(self):
        return self.filter(status=Borrow.Status.BORROWED, return_date__isnull=True)

    def returned(self):
        return self.filter(status=Borrow.Status.RETURNED)

    def overdue(self):
        today = timezone.localdate()
        return self.filter(status=Borrow.Status.BORROWED, return_date__isnull=True, due_date__lt=today)


class BorrowManager(models.Manager):
    def get_queryset(self):
        return BorrowQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def returned(self):
        return self.get_queryset().returned()

    def overdue(self):
        return self.get_queryset().overdue()


class Book(models.Model):
    """Book model for inventory management."""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(
        max_length=13,
        unique=True,
        help_text='International Standard Book Number'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='books'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Book price must be greater than 0'
    )
    stock_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Stock quantity cannot be negative'
    )
    publication_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Custom manager
    objects = BookManager()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author']),
            models.Index(fields=['isbn']),
        ]

    def __str__(self):
        return f"{self.title} by {self.author}"

    @property
    def inventory_value(self):
        """Calculate the inventory value for this book."""
        return self.price * self.stock_quantity

    @property
    def stock_status(self):
        """Return the stock status as a string."""
        if self.stock_quantity == 0:
            return 'Out of Stock'
        elif self.stock_quantity <= 10:
            return 'Low Stock'
        else:
            return 'In Stock'

    @property
    def stock_badge_class(self):
        """Return Bootstrap badge class for stock status."""
        if self.stock_quantity == 0:
            return 'danger'
        elif self.stock_quantity <= 10:
            return 'warning'
        else:
            return 'success'


class Borrow(models.Model):
    """Borrow record linking a user to a borrowed book."""

    class Status(models.TextChoices):
        BORROWED = 'Borrowed', 'Borrowed'
        RETURNED = 'Returned', 'Returned'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='borrows'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='borrows'
    )
    borrow_date = models.DateField(default=timezone.localdate)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.BORROWED)
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BorrowManager()

    class Meta:
        ordering = ['-borrow_date', '-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['borrow_date']),
            models.Index(fields=['due_date']),
        ]

    def __str__(self):
        user_label = self.user.username if self.user else 'Deleted User'
        book_label = self.book.title if self.book else 'Deleted Book'
        return f'{book_label} borrowed by {user_label}'

    @property
    def is_overdue(self):
        return self.status == self.Status.BORROWED and self.return_date is None and self.due_date < timezone.localdate()

    @property
    def display_status(self):
        if self.status == self.Status.RETURNED:
            return self.Status.RETURNED
        if self.is_overdue:
            return 'Overdue'
        return self.Status.BORROWED
