from django.urls import path
from .views import telescope_log_view, success_view, log_data_view, session_detail_view, delete_log_view, fetch_weather_data

urlpatterns = [
    path('', telescope_log_view, name='telescope_log'),
    path("get-weather-data/", fetch_weather_data, name="get_weather_data"),
    path('logs/', log_data_view, name='log_data'),
    path('success/', success_view, name='success'),
    path('session/<str:session_id>/', session_detail_view, name='session_detail'),
    path('delete/<str:session_id>/', delete_log_view, name='delete_log'),
]