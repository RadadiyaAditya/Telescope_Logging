from django.urls import path
from .views import (telescope_log_view, success_view, log_data_view, session_detail_view, 
                    fetch_weather_data, generate_pdf, send_email, fits_view, download_multi_pdf,
                    fetch_telescope_data)


#: URL patterns for the telescope logging system.
#: 
#: Each path maps a route to a specific view function:
#:
#: - '' → telescope_log_view: Main logging form
#: - 'get-weather-data/' → fetch_weather_data: API for live weather data
#: - 'logs/' → log_data_view: Log list with filters
#: - 'success/' → success_view: Success page
#: - 'session/<session_id>/' → session_detail_view: Detailed view of a specific log session
#: - 'download-pdf/<session_id>/' → generate_pdf: PDF download for a session
#: - 'send-email/<session_id>/' → send_email: Email a session's PDF
#: - 'fits/' → fits_view: FITS upload and metadata injection

urlpatterns = [
    path('', telescope_log_view, name='telescope_log'),
    path("get-weather-data/", fetch_weather_data, name="get_weather_data"),
    path("get-telescope-data/", fetch_telescope_data, name="get_telescope_data"),
    path('logs/', log_data_view, name='log_data'),
    path('success/', success_view, name='success'),
    path('session/<str:session_id>/', session_detail_view, name='session_detail'),
    path('download-pdf/<str:session_id>/', generate_pdf, name='download_pdf'),
    path('send-email/<str:session_id>/', send_email, name='send_email'),
    path('send-email/', send_email, name='send_email'),
    path('fits/', fits_view, name='fits_page'),
    path('download-multi-pdf/', download_multi_pdf, name='download_multi_pdf')
]