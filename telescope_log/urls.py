"""
URL configuration for telescope_log project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

"""
Main URL configuration for the Telescope Logging Django project.

This file defines route mappings for:
- Admin interface
- User registration, login, logout, profile
- Telescope log system views (included from logging_system.urls)
- Static file handling in development
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users import views as user_views

# Route definitions for admin, user auth, and logging system
urlpatterns = [
    path('admin/', admin.site.urls),    # Admin interface for managing the site
    path('register/', user_views.register, name='register'),    # User registration page
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),   # User login page
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),   # User logout page
    path('profile/', user_views.profile, name='profile'),   
    path('', include('logging_system.urls')),  # Include the logging system URLs
]

# Static file route (for development only)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)