from django.urls import path
from .views import (telescope_log_view, success_view, log_data_view, session_detail_view, 
                    fetch_weather_data, generate_pdf, send_email, fits_view)

urlpatterns = [
    path('', telescope_log_view, name='telescope_log'),
    path("get-weather-data/", fetch_weather_data, name="get_weather_data"),
    path('logs/', log_data_view, name='log_data'),
    path('success/', success_view, name='success'),
    path('session/<str:session_id>/', session_detail_view, name='session_detail'),
    path('download-pdf/<str:session_id>/', generate_pdf, name='download_pdf'),
    path('send-email/<str:session_id>/', send_email, name='send_email'),
    path('fits/', fits_view, name='fits_page'),
]