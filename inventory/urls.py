from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Landing page
    path('', views.landing, name='landing'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('borrow/issue/', views.issue_book, name='issue_book'),
    path('borrow/<int:pk>/return/', views.return_book, name='return_book'),
    
    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Book URLs
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_create, name='book_create'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    
    # Inventory URLs
    path('inventory/', views.inventory, name='inventory'),
    
    # Auth URLs
    path('auth/login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/register/', views.register, name='register'),
]
