from django.urls import path
from .views import telescope_log_view, success_view, log_data_view, session_detail_view

urlpatterns = [
    path('', telescope_log_view, name='telescope_log'),
    path('logs/', log_data_view, name='log_data'),
    path('success/', success_view, name='success'),
    path('session/<str:session_id>/', session_detail_view, name='session_detail'),
]