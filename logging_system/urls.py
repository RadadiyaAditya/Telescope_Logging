from django.urls import path
from .views import telescope_log_view, success_view

urlpatterns = [
    path('', telescope_log_view, name='telescope_log'),
    path('success/', success_view, name='success'),
]