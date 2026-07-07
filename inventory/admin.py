from django.contrib import admin
from .models import Category, Book, Borrow


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin configuration for Book model."""
    list_display = ['title', 'author', 'isbn', 'category', 'price', 'stock_quantity', 'created_at']
    list_filter = ['category', 'created_at', 'publication_date']
    search_fields = ['title', 'author', 'isbn']
    list_per_page = 20
    readonly_fields = ['created_at', 'updated_at', 'inventory_value']
    
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'isbn', 'category', 'publication_date')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock_quantity', 'inventory_value')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def inventory_value(self, obj):
        """Display inventory value in admin."""
        return f"${obj.inventory_value:,.2f}"
    inventory_value.short_description = 'Inventory Value'


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'borrow_date', 'due_date', 'return_date', 'status', 'fine']
    list_filter = ['status', 'borrow_date', 'due_date', 'return_date']
    search_fields = ['book__title', 'book__isbn', 'user__username', 'user__email']
    autocomplete_fields = ['book', 'user']
    list_select_related = ['book', 'user']
