from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .forms import (
    GeneralInfoForm, EnvironmentalConditionForm, TelescopeConfigurationForm,
    ObservationForm, InstrumentationForm, RemoteOperationForm, CommentForm
)
import os
from .models import GeneralInfo
import requests
from django.http import JsonResponse
from dotenv import load_dotenv

from bs4 import BeautifulSoup
from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
import pdfkit
import os

load_dotenv()

# Create your views here.

# Main form view
@login_required
def telescope_log_view(request):

    if request.method == 'POST':
        general_form = GeneralInfoForm(request.POST)
        env_form = EnvironmentalConditionForm(request.POST)
        telescope_form = TelescopeConfigurationForm(request.POST)
        observation_form = ObservationForm(request.POST)
        instrumentation_form = InstrumentationForm(request.POST)
        remote_form = RemoteOperationForm(request.POST)
        comment_form = CommentForm(request.POST)


        if (general_form.is_valid() and env_form.is_valid() and telescope_form.is_valid() and
            observation_form.is_valid() and instrumentation_form.is_valid() and remote_form.is_valid() and
            comment_form.is_valid()):


            general_instance = general_form.save(commit=False)
            general_instance.observer_name = request.user  # Autofill with logged-in user
            general_instance.save()
            
            # For each related form, use commit=False, then set general_info.
            env_instance = env_form.save(commit=False)
            env_instance.general_info = general_instance
            env_instance.save()
            
            telescope_instance = telescope_form.save(commit=False)
            telescope_instance.general_info = general_instance
            telescope_instance.save()
            
            observation_instance = observation_form.save(commit=False)
            observation_instance.general_info = general_instance
            observation_instance.save()
            
            instrumentation_instance = instrumentation_form.save(commit=False)
            instrumentation_instance.general_info = general_instance
            instrumentation_instance.save()
            
            remote_instance = remote_form.save(commit=False)
            remote_instance.general_info = general_instance
            remote_instance.save()
            
            comment_instance = comment_form.save(commit=False)
            comment_instance.general_info = general_instance
            comment_instance.save()

            if 'download_pdf' in request.POST:
                return generate_pdf(general_instance)

            messages.success(request, 'Log Saved Successfully')  # Redirect to a success page after saving
            return redirect('telescope_log')

    else:
        general_form = GeneralInfoForm()
        env_form = EnvironmentalConditionForm()
        telescope_form = TelescopeConfigurationForm()
        observation_form = ObservationForm()
        instrumentation_form = InstrumentationForm()
        remote_form = RemoteOperationForm()
        comment_form = CommentForm()

    return render(request, 'logging_system/telescope_log.html', {
        'general_form': general_form,
        'env_form': env_form,
        'telescope_form': telescope_form,
        'observation_form': observation_form,
        'instrumentation_form': instrumentation_form,
        'remote_form': remote_form,
        'comment_form': comment_form,
    })


def generate_pdf(request, session_id):
    """Generate a PDF containing only the tables from session_detail.html."""

    # Define the path for wkhtmltopdf
    wkhtmltopdf_path = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"

    # Ensure wkhtmltopdf exists
    if not os.path.exists(wkhtmltopdf_path):
        return HttpResponse(f"Error: wkhtmltopdf not found at {wkhtmltopdf_path}", status=500)

    try:
        # Retrieve session details
        general_instance = get_object_or_404(GeneralInfo, session_id=session_id)

        context = {
            'general': general_instance,
            'environmental_condition': getattr(general_instance, 'environmental_condition', None),
            'observation': getattr(general_instance, 'observation', None),
            'telescope_configuration': getattr(general_instance, 'telescope_configuration', None),
            'instrumentation': getattr(general_instance, 'instrumentation', None),
            'remote_operation': getattr(general_instance, 'remote_operation', None),
            'comments': getattr(general_instance, 'comments', None),
        }

        # ✅ Render full session_detail.html
        full_html = render_to_string('logging_system/session_detail.html', context)

        # ✅ Extract only <table> elements using BeautifulSoup
        soup = BeautifulSoup(full_html, "html.parser")
        tables = soup.find_all("table")
        table_titles = [
            "GENERAL INFORMATION", "WEATHER CONDITIONS", "OBSERVATION PARAMETERS",
            "TELESCOPE CONFIGURATION", "INSTRUMENTATION", "REMOTE OPERATION", "COMMENTS"
        ]

          # Inline CSS for table formatting
        styles = """
        <style>
            body { font-family: Arial, sans-serif; }
            h2 { text-align: center; margin-bottom: 20px; }
            table { width: 100%; border-collapse: collapse; margin-bottom: 15px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; font-weight: bold; }
            .table-container { margin: auto; width: 80%; }
        </style>
        """


        # Construct final HTML
        table_html = f"<h2>Log Session: {session_id}</h2>{styles}<div class='container'>"
        for title, table in zip(table_titles, tables):
            table_html += f"<div class='table-box'><h3>{title}</h3>{str(table)}</div>"
        table_html += "</div>"

        # PDF options for better formatting
        pdf_options = {
            'page-size': 'A4',
            'encoding': 'UTF-8',
            'margin-top': '10mm',
            'margin-right': '10mm',
            'margin-bottom': '10mm',
            'margin-left': '10mm'
        }
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        # Generate PDF
        temp_pdf_path = f"Log_{session_id}.pdf"
        pdfkit.from_string(table_html, temp_pdf_path, options=pdf_options, configuration=config)

        # ✅ Return FileResponse without closing it early
        return FileResponse(open(temp_pdf_path, "rb"), as_attachment=True, filename=f"Log_{session_id}.pdf")

    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)

def fetch_weather_data(request):
    """Fetch weather data from API and return JSON response."""
    api_key = os.getenv("Weather_API")
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q=24.6528,72.7794"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return JsonResponse({
            "temperature": data['current']['temp_c'],
            "humidity": data['current']['humidity'],
            "wind_speed": round(data['current']['wind_kph'] / 3.6, 2),
            "cloud_cover": data['current']['cloud']
        })
    else:
        return JsonResponse({"error": "Failed to fetch weather data"}, status=500)

# Success view upon submitting form
def success_view(request):
    return render(request, 'logging_system/success.html')

# Logs Webpage
@login_required
def log_data_view(request):

    session_id = request.GET.get('session_id', '')
    operator_name = request.GET.get('operator_name', '')
    instrument_name = request.GET.get('instrument_name', '')
    target_name = request.GET.get('target_name', '')
    date_filter = request.GET.get('date', '')

    # Retrieve all log entries, ordering by the latest start time first
    logs = (
        GeneralInfo.objects.all()
        .order_by('-log_start_time_utc')
        .select_related(
            'environmental_condition',
            'observation',
            'telescope_configuration',
            'instrumentation',
            'remote_operation',
            'comments'
        )
    )

    filters = Q()

    if session_id:
        filters &= Q(session_id__icontains=session_id)
    
    if operator_name:
        filters &= Q(operator_name__icontains=operator_name)

    if instrument_name:
        filters &= Q(instrumentation__instrument_name__icontains=instrument_name)

    if target_name:
        filters &= Q(observation__target_name__icontains=target_name)

    if date_filter:
        filters &= Q(log_start_time_utc__date=date_filter)

    logs = logs.filter(filters)

    context = {
        'logs': logs,
        'session_id': session_id,
        'operator_name': operator_name,
        'instrument_name': instrument_name,
        'target_name': target_name,
        'date_filter': date_filter,
    }

    return render(request, 'logging_system/log_data.html', context)


# detailed view of logs
@login_required
def session_detail_view(request, session_id):
    # Retrieve the main GeneralInfo record using the unique session_id.
    general = get_object_or_404(GeneralInfo, session_id=session_id)
    
    # Retrieve the related one-to-one objects using the related_name specified in your models.
    # Use getattr() with a default of None in case a related record doesn't exist.
    environmental_condition = getattr(general, 'environmental_condition', None)
    observation = getattr(general, 'observation', None)
    telescope_configuration = getattr(general, 'telescope_configuration', None)
    instrumentation = getattr(general, 'instrumentation', None)
    remote_operation = getattr(general, 'remote_operation', None)
    comments = getattr(general, 'comments', None)
    
    context = {
        'general': general,
        'environmental_condition': environmental_condition,
        'observation': observation,
        'telescope_configuration': telescope_configuration,
        'instrumentation': instrumentation,
        'remote_operation': remote_operation,
        'comments': comments,
    }
    return render(request, 'logging_system/session_detail.html', context)
