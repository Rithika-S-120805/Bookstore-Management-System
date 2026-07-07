from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Category, Book


class CategoryForm(forms.ModelForm):
    """Form for creating and editing categories."""
    
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category description',
                'rows': 4
            }),
        }

    def clean_name(self):
        """Validate category name is unique."""
        name = self.cleaned_data.get('name')
        if name:
            # Check if name exists (excluding current object in edit mode)
            qs = Category.objects.filter(name__iexact=name)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('A category with this name already exists.')
        return name


class BookForm(forms.ModelForm):
    """Form for creating and editing books."""
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'category', 'price', 'stock_quantity', 'publication_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter ISBN (13 digits)',
                'maxlength': '13'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price',
                'step': '0.01',
                'min': '0.01'
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter stock quantity',
                'min': '0'
            }),
            'publication_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def clean_isbn(self):
        """Validate ISBN format and uniqueness."""
        isbn = self.cleaned_data.get('isbn')
        if isbn:
            # Check if ISBN is 13 digits
            if not isbn.isdigit() or len(isbn) != 13:
                raise ValidationError('ISBN must be exactly 13 digits.')
            
            # Check if ISBN already exists
            qs = Book.objects.filter(isbn=isbn)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('A book with this ISBN already exists.')
        return isbn

    def clean_price(self):
        """Validate price is positive."""
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise ValidationError('Price must be greater than zero.')
        return price

    def clean_stock_quantity(self):
        """Validate stock quantity is non-negative."""
        stock = self.cleaned_data.get('stock_quantity')
        if stock is not None and stock < 0:
            raise ValidationError('Stock quantity cannot be negative.')
        return stock


class BorrowIssueForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    book = forms.ModelChoiceField(
        queryset=Book.objects.select_related('category').all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date is not None and due_date < timezone.localdate():
            raise ValidationError('Due date cannot be in the past.')
        return due_date
