"""
Views for the Telescope Logging System.

Handles:
- Multi-section form submission (general info, weather, telescope, observation, etc.)
- PDF generation and download
- Email sending with PDF attachment via SMTP or app email
- FITS file upload and metadata injection
- Log listing, filtering, and detail views
- Weather data retrieval from API
"""


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .forms import (
    GeneralInfoForm, EnvironmentalConditionForm, TelescopeConfigurationForm,
    ObservationForm, InstrumentationForm, RemoteOperationForm, CommentForm, EmailForm,
    FitsUploadForm
)
import os
from .models import GeneralInfo
import requests
from django.http import JsonResponse
import json
from dotenv import load_dotenv

#required for downloading pdf
from django.http import FileResponse, HttpResponse
import tempfile
from .report_utils import generate_pdf_reportlab, build_report_story
from django.views.decorators.http import require_POST
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm


import csv

#required for sending email
from django.core.mail import EmailMessage
from .forms import EmailForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

#required for fits file editing
import io
from astropy.io import fits

load_dotenv()

# Create your views here.

# Main form view
@login_required
def telescope_log_view(request):

    """
    Main view for submitting telescope observation logs.

    Handles multiple forms for different sections:
    - General session info
    - Environmental conditions
    - Telescope configuration
    - Observational parameters
    - Instrumentation
    - Remote operation
    - Comments
    - Email recipient entry

    Supports PDF generation and email dispatch.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered form or redirect with success/failure messages.
    """

    if request.method == 'POST':
        general_form = GeneralInfoForm(request.POST)
        env_form = EnvironmentalConditionForm(request.POST)
        telescope_form = TelescopeConfigurationForm(request.POST)
        observation_form = ObservationForm(request.POST)
        instrumentation_form = InstrumentationForm(request.POST)
        remote_form = RemoteOperationForm(request.POST)
        comment_form = CommentForm(request.POST)
        email_form = EmailForm(request.POST)


        print("POST received")
        print("GeneralInfoForm errors:", general_form.errors)
        print("EnvForm errors:", env_form.errors)
        print("TelescopeForm errors:", telescope_form.errors)
        print("ObservationForm errors:", observation_form.errors)
        print("InstrumentationForm errors:", instrumentation_form.errors)
        print("RemoteForm errors:", remote_form.errors)
        print("CommentForm errors:", comment_form.errors)
        print("POST data:", request.POST)

        if (general_form.is_valid() and env_form.is_valid() and telescope_form.is_valid() and
            observation_form.is_valid() and instrumentation_form.is_valid() and remote_form.is_valid() and
            comment_form.is_valid()):


            general_instance = general_form.save(commit=False)
            general_instance.observer_name = request.user  # Autofill with logged-in user
            general_instance.save()

            session_id = general_instance.session_id
            
            # For each related form, use commit=False, then set general_info.
            env_instance = env_form.save(commit=False)
            env_instance.general_info = general_instance
            env_instance.save()
            
            telescope_instance = telescope_form.save(commit=False)
            telescope_instance.general_info = general_instance
            telescope_instance.save()
            

            observation_instance = observation_form.save(commit=False)
            observation_instance.right_ascension = observation_form.cleaned_data['right_ascension']
            observation_instance.declination = observation_form.cleaned_data['declination']
            observation_instance.general_info = general_instance
            observation_instance.save()
            
            instrumentation_instance = instrumentation_form.save(commit=False)
            if instrumentation_form.cleaned_data['filter_in_use'] == 'Enter Manually':
                instrumentation_instance.filter_in_use = instrumentation_form.cleaned_data['custom_filter']
            instrumentation_instance.general_info = general_instance
            instrumentation_instance.save()
                        
            remote_instance = remote_form.save(commit=False)
            remote_instance.general_info = general_instance
            remote_instance.save()
            
            comment_instance = comment_form.save(commit=False)
            comment_instance.general_info = general_instance
            comment_instance.save()

            # create or append log data to .csv file
            append_log_to_csv(general_instance)
            

            messages.success(request, f'Log Saved Successfully — Session ID: {session_id}')
            return redirect('telescope_log')

    else:
        general_form = GeneralInfoForm()
        env_form = EnvironmentalConditionForm()
        telescope_form = TelescopeConfigurationForm()
        observation_form = ObservationForm()
        instrumentation_form = InstrumentationForm()
        remote_form = RemoteOperationForm()
        comment_form = CommentForm()
        email_form = EmailForm()

    return render(request, 'logging_system/telescope_log.html', {
        'general_form': general_form,
        'generated_session_id': locals().get('session_id', None),
        'env_form': env_form,
        'telescope_form': telescope_form,
        'observation_form': observation_form,
        'instrumentation_form': instrumentation_form,
        'remote_form': remote_form,
        'comment_form': comment_form,
        'email_form': email_form,
    })

# Fetch telescope data from JSON file
def fetch_telescope_data(request):
    """
    Fetch the latest telescope serial data from JSON.
    """
    try:
        with open("latest_serial_data.json", "r") as f:
            data = json.load(f)
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({"error": "Failed to read telescope data: " + str(e)}, status=500)

# Create PDF file from HTML template
def create_pdf_file(session_id):
    """
    Generate a PDF log file for a given session ID.

    Args:
        session_id (int): The unique session identifier.

    Returns:
        str: Path to the generated PDF file.
    """

    general_instance = get_object_or_404(GeneralInfo, session_id=session_id)

    # Prepare structured data for reportlab
    session_data = {
        "session_id": general_instance.session_id,
        "general": {
            "telescope_name": general_instance.telescope_name,
            "telescope_operator": general_instance.telescope_operator,
            "observer_name": general_instance.observer_name,
            "log_start_time_utc": general_instance.log_start_time_utc.strftime("%B %d, %Y, %I:%M:%S %p"),
            "log_start_time_lst": general_instance.log_start_time_lst.strftime("%B %d, %Y, %I:%M:%S %p"),
            "log_end_time_utc": general_instance.log_end_time_utc.strftime("%B %d, %Y, %I:%M:%S %p"),
            "log_end_time_lst": general_instance.log_end_time_lst.strftime("%B %d, %Y, %I:%M:%S %p"),
        },
        "weather": {
            "temperature": getattr(general_instance.environmental_condition, "temperature", ""),
            "humidity": getattr(general_instance.environmental_condition, "humidity", ""),
            "wind_speed": getattr(general_instance.environmental_condition, "wind_speed", ""),
            "seeing": getattr(general_instance.environmental_condition, "seeing", ""),
            "cloud_coverage": getattr(general_instance.environmental_condition, "cloud_coverage", ""),
            "moon_phase": getattr(general_instance.environmental_condition, "moon_phase", ""),
        },
        "observation": {
            "target_name": getattr(general_instance.observation, "target_name", ""),
            "right_ascension": getattr(general_instance.observation, "right_ascension", ""),
            "declination": getattr(general_instance.observation, "declination", ""),
            "magnitude": getattr(general_instance.observation, "magnitude", ""),
        },
        "telescope": {
            "focus_position": getattr(general_instance.telescope_configuration, "focus_position", ""),
            "air_mass": getattr(general_instance.telescope_configuration, "air_mass", ""),
            "tracking_mode": getattr(general_instance.telescope_configuration, "tracking_mode", ""),
            "guiding_status": getattr(general_instance.telescope_configuration, "guiding_status", ""),
        },
        "instrument": {
            "instrument_name": getattr(general_instance.instrumentation, "instrument_name", ""),
            "observing_mode": getattr(general_instance.instrumentation, "observing_mode", ""),
            "calibration": getattr(general_instance.instrumentation, "calibration", ""),
            "filter_in_use": getattr(general_instance.instrumentation, "filter_in_use", ""),
            "exposure_time": getattr(general_instance.instrumentation, "exposure_time", ""),
            "polarization_mode": getattr(general_instance.instrumentation, "polarization_mode", ""),
        },
        "remote": {
            "remote_access": getattr(general_instance.remote_operation, "remote_access", ""),
            "remote_observer": getattr(general_instance.remote_operation, "remote_observer", ""),
            "emergency_stop": getattr(general_instance.remote_operation, "emergency_stop", ""),
        },
        "comments": {
            "comments": getattr(general_instance.comments, "comments", ""),
        }
    }

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as log_file:
        generate_pdf_reportlab(session_data, log_file.name)
        return log_file.name

# Generate PDF and return it as a FileResponse for download
def generate_pdf(request, session_id):
    """
    Serve a generated PDF file as a downloadable response.

    Args:
        request (HttpRequest): The HTTP request object.
        session_id (int): The unique session ID.

    Returns:
        FileResponse: A response with the PDF file attached.
    """
    general = get_object_or_404(GeneralInfo, session_id=session_id)
    pdf_path = create_pdf_file(session_id)
    if not pdf_path or not os.path.exists(pdf_path):
        return HttpResponse("Error generating PDF.", status=500)

    pdf_file = open(pdf_path, 'rb')
    response = FileResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Log-{general.telescope_name}-{general.log_start_time_utc.strftime('%Y-%m-%d')}.pdf"'
    return response

# Send email with PDF attachment 
def send_email(request, session_id=None):

    # Check if this is a multi-session email request

    session_ids = request.POST.getlist("session_ids")
    if session_ids:
        general = None  # no single session context
        
        session_list = ", ".join(session_ids)
        log_reference = f"Log-{session_list}"
        #Build email body (based on first session if multiple)
        first_session = get_object_or_404(GeneralInfo, session_id=session_ids[0])
        subject = f"{first_session.telescope_name} Log Report - {first_session.log_start_time_utc.strftime('%d %B %Y')}"
        email_body = f"""
        <html><body>
        <p>Dear User,</p>
        <p>Please find attached the telescope log report for the selected sessions - {log_reference}.</p>
        <p>Best regards,<br>Telescope Logging System</p>
        </body></html>
        """
    else:
        # Fallback: treat it as a single session email
        session_ids = [session_id]
        general = get_object_or_404(GeneralInfo, session_id=session_id)

        # Create the email body
        subject = f"{general.telescope_name} Log - {general.log_start_time_utc.strftime('%d %B %Y')}"
        email_body = f"""
        <html>
        <head></head>
        <body>
            <p>Dear User,</p>
            <p>Please find attached the telescope log report for the log session {general.telescope_name}-{general.log_start_time_utc.strftime('%Y-%m-%d')}.</p>
            <h3>Session Details:</h3>
            <ul>
                <li><strong>Session ID:</strong> {general.session_id}</li>
                <li><strong>Telescope:</strong> {general.telescope_name}</li>
                <li><strong>Operator:</strong> {general.telescope_operator}</li>
                <li><strong>Observer:</strong> {general.observer_name}</li>
                <li><strong>Log Start Time (UTC):</strong> {general.log_start_time_utc.strftime('%Y-%m-%d %H:%M:%S')}</li>
                <li><strong>Log Date:</strong> {general.log_start_time_utc.strftime('%d %B %Y')}</li>
                <li><strong>Instrument:</strong> {getattr(general.instrumentation, 'instrument_name', 'N/A')}</li>
                <li><strong>Exposure Time:</strong> {getattr(general.instrumentation, 'exposure_time', 'N/A')} seconds</li>
                <li><strong>Target Object:</strong> {getattr(general.observation, 'target_name', 'N/A')}</li>
                <li><strong>Airmass:</strong> {getattr(general.telescope_configuration, 'air_mass', 'N/A')}</li>
                <li><strong>Seeing:</strong> {getattr(general.environmental_condition, 'seeing', 'N/A')}</li>
            </ul>
            <p>Best regards,<br>Telescope Logging System</p>
        </body>
        </html>
        """


    # predifined recipient list (Admin & miro)

    recipient_list = [
        "miro@prl.res.in",
        request.user.email
    ]


    # additional recipient email and thier validation
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            additional_email = request.session.pop("recipient_email", None) or request.POST.get("recipient_email")
            if additional_email:
                email_list = [email.strip() for email in additional_email.split(",") if email.strip()]
                
                # Validate each email
                for email in email_list:
                    try:
                        validate_email(email)
                    except ValidationError:
                        messages.error(request, f"Invalid email address: {email}")
                        return redirect("session_detail", session_id=session_id) if session_id else redirect("log_data")
                
                
                recipient_list.extend(email_list)

    
    # Generate PDF (combined if multiple sessions)
    story = []
    for sid in session_ids:
        instance = get_object_or_404(GeneralInfo, session_id=sid)
        session_data = prepare_session_data(instance)
        build_report_story(session_data, story)

    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(A4),
                            rightMargin=1*cm, leftMargin=1*cm,
                            topMargin=1*cm, bottomMargin=1*cm)
    doc.build(story)
    pdf_buffer.seek(0)


    # get sender's email and password
    if request.method == "POST":
        smtp_user = request.session.pop("smtp_user", None) or request.POST.get("smtp_user")
        smtp_email = request.user.email
        smtp_password = request.session.pop("smtp_password", None) or request.POST.get("smtp_password")


    # send email from the sender's email to the recipient list
        try:
            msg = MIMEMultipart()
            msg["From"] = smtp_email
            msg["To"] = ", ".join(recipient_list)
            msg["Subject"] = subject
            msg.attach(MIMEText(email_body, "html"))


            part = MIMEApplication(pdf_buffer.read(), _subtype="pdf")
            if general:
                filename = f"Log-{general.telescope_name}-{general.log_start_time_utc.strftime('%Y-%m-%d')}.pdf"
            else:
                filename = f"Combined_Logs_{session_ids[0]}_to_{session_ids[-1]}.pdf"    
            part.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(part)

            with smtplib.SMTP(os.getenv("SMTP_DOMAIN"), os.getenv("SMTP_PORT")) as server:  # Update your domain and port 'start tls'
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
            
            

            if request.session.pop("return_to_log", False):
                messages.success(request, f"Email sent successfully to {', '.join(recipient_list)}.")
                return redirect("telescope_log")
            else:
                messages.success(request, f"Email sent successfully to {', '.join(recipient_list)}.")
                request.session.pop("recipient_email", None)
                return redirect("session_detail", session_id=session_id) if session_id else redirect("log_data")

        except Exception as e:
            messages.error(request, f"Failed to send email: {str(e)}")
            return redirect("session_detail", session_id=session_id) if session_id else redirect("log_data")

    if session_id:
        messages.success(request, f"Email sent successfully to {', '.join(recipient_list)}.")
        request.session.pop("recipient_email", None)
        return redirect("session_detail", session_id=session_id)
    else:
        messages.success(request, f"Email conatining logs - {session_list} sent successfully to {', '.join(recipient_list)}.")
        request.session.pop("recipient_email", None)
        return redirect("log_data")

# Fetch weather data from API
def fetch_weather_data(request):
    """
    Fetch current weather data from the WeatherAPI and return as JSON.

    Returns:
        JsonResponse: Dictionary containing temperature, humidity, wind speed, and cloud cover.
    """

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
    """
    Render the success page after form submission.

    Returns:
        HttpResponse: Rendered success.html template.
    """
    return render(request, 'logging_system/success.html')

# Logs Webpage
@login_required
def log_data_view(request):

    """
    Render the logs list page with filtering support.

    Filters supported:
    - session_id
    - observer_name
    - instrument_name
    - target_name
    - date

    Returns:
        HttpResponse: Rendered log_data.html with filtered logs.
    """

    session_id = request.GET.get('session_id', '')
    observer_name = request.GET.get('observer_name', '')
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
    
    if observer_name:
        filters &= Q(observer_name__username__icontains=observer_name)

    if instrument_name:
        filters &= Q(instrumentation__instrument_name__icontains=instrument_name)

    if target_name:
        filters &= Q(observation__target_name__icontains=target_name)

    if date_filter:
        filters &= Q(log_start_time_utc__date=date_filter)

    logs = logs.filter(filters)
    email_form = EmailForm()

    context = {
        'logs': logs,
        'session_id': session_id,
        'observer_name': observer_name,
        'instrument_name': instrument_name,
        'target_name': target_name,
        'date_filter': date_filter,
        'email_form': email_form, 
    }

    return render(request, 'logging_system/log_data.html', context)


# detailed view of logs
@login_required
def session_detail_view(request, session_id):

    """
    Render the detailed view for a specific observation session.

    Args:
        request (HttpRequest): Incoming request object.
        session_id (int): Unique ID for the session.

    Returns:
        HttpResponse: Rendered session_detail.html template with session data.
    """
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
    email_form = EmailForm()
    
    context = {
        'general': general,
        'environmental_condition': environmental_condition,
        'observation': observation,
        'telescope_configuration': telescope_configuration,
        'instrumentation': instrumentation,
        'remote_operation': remote_operation,
        'comments': comments,
        'email_form': email_form,
    }
    return render(request, 'logging_system/session_detail.html', context)

# Prepare session data for PDF generation
def prepare_session_data(general_instance):
    return {
        "session_id": general_instance.session_id,
        "general": {
            "telescope_name": general_instance.telescope_name,
            "telescope_operator": general_instance.telescope_operator,
            "observer_name": general_instance.observer_name,
            "log_start_time_utc": general_instance.log_start_time_utc.strftime("%B %d, %Y, %I:%M:%S %p"),
            "log_start_time_lst": general_instance.log_start_time_lst.strftime("%B %d, %Y, %I:%M:%S %p"),
            "log_end_time_utc": general_instance.log_end_time_utc.strftime("%B %d, %Y, %I:%M:%S %p"),
            "log_end_time_lst": general_instance.log_end_time_lst.strftime("%B %d, %Y, %I:%M:%S %p"),
        },
        "weather": {
            "temperature": getattr(general_instance.environmental_condition, "temperature", ""),
            "humidity": getattr(general_instance.environmental_condition, "humidity", ""),
            "wind_speed": getattr(general_instance.environmental_condition, "wind_speed", ""),
            "seeing": getattr(general_instance.environmental_condition, "seeing", ""),
            "cloud_coverage": getattr(general_instance.environmental_condition, "cloud_coverage", ""),
            "moon_phase": getattr(general_instance.environmental_condition, "moon_phase", ""),
        },
        "observation": {
            "target_name": getattr(general_instance.observation, "target_name", ""),
            "right_ascension": getattr(general_instance.observation, "right_ascension", ""),
            "declination": getattr(general_instance.observation, "declination", ""),
            "magnitude": getattr(general_instance.observation, "magnitude", ""),
        },
        "telescope": {
            "focus_position": getattr(general_instance.telescope_configuration, "focus_position", ""),
            "air_mass": getattr(general_instance.telescope_configuration, "air_mass", ""),
            "tracking_mode": getattr(general_instance.telescope_configuration, "tracking_mode", ""),
            "guiding_status": getattr(general_instance.telescope_configuration, "guiding_status", ""),
        },
        "instrument": {
            "instrument_name": getattr(general_instance.instrumentation, "instrument_name", ""),
            "observing_mode": getattr(general_instance.instrumentation, "observing_mode", ""),
            "calibration": getattr(general_instance.instrumentation, "calibration", ""),
            "filter_in_use": getattr(general_instance.instrumentation, "filter_in_use", ""),
            "exposure_time": getattr(general_instance.instrumentation, "exposure_time", ""),
            "polarization_mode": getattr(general_instance.instrumentation, "polarization_mode", ""),
        },
        "remote": {
            "remote_access": getattr(general_instance.remote_operation, "remote_access", ""),
            "remote_observer": getattr(general_instance.remote_operation, "remote_observer", ""),
            "emergency_stop": getattr(general_instance.remote_operation, "emergency_stop", ""),
        },
        "comments": {
            "comments": getattr(general_instance.comments, "comments", ""),
        }
    }

# Multiple-pdf download
@require_POST
def download_multi_pdf(request):
    session_ids = request.POST.getlist('session_ids')
    if not session_ids:
        messages.error(request, "Please select at least one session to download.")
        return redirect('log_data')

    story = []
    for session_id in session_ids:
        general = get_object_or_404(GeneralInfo, session_id=session_id)
        session_data = prepare_session_data(general)
        build_report_story(session_data, story)  # Append per session

    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_pdf.name, pagesize=landscape(A4),
                            rightMargin=1*cm, leftMargin=1*cm,
                            topMargin=1*cm, bottomMargin=1*cm)
    doc.build(story)

    filename = f"Logs_Session_{session_ids[0]}_to_{session_ids[-1]}.pdf"

    return FileResponse(
        open(temp_pdf.name, "rb"),
        as_attachment=True,
        filename=filename,
        content_type="application/pdf"
    )


# Append log data to CSV file
def append_log_to_csv(general_info):
    """
    Appends a single observation session to the logs.csv file.
    """

    csv_dir = os.getenv("CSV_LOG_PATH", "csv_logs")
    csv_file_path = os.path.join(csv_dir, "telescope_logs.csv")  # Adjust path as needed
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

    # Preparing the data row
    row = [
        general_info.session_id,
        general_info.telescope_name,
        general_info.telescope_operator,
        general_info.observer_name.username,
        general_info.log_start_time_utc.strftime("%Y-%m-%d %H:%M:%S"),
        general_info.log_start_time_lst.strftime("%Y-%m-%d %H:%M:%S"),
        general_info.log_end_time_utc.strftime("%Y-%m-%d %H:%M:%S"),
        general_info.log_end_time_lst.strftime("%Y-%m-%d %H:%M:%S"),


        getattr(general_info.observation, "target_name", ""),
        getattr(general_info.observation, "right_ascension", ""),
        getattr(general_info.observation, "declination", ""),
        getattr(general_info.observation, "magnitude", ""),


        getattr(general_info.instrumentation, "instrument_name", ""),
        getattr(general_info.instrumentation, "observing_mode", ""),
        getattr(general_info.instrumentation, "exposure_time", ""),
        getattr(general_info.instrumentation, "calibration", ""),
        getattr(general_info.instrumentation, "filter_in_use", ""),
        getattr(general_info.instrumentation, "polarization_mode", ""),


        getattr(general_info.environmental_condition, "temperature", ""),
        getattr(general_info.environmental_condition, "humidity", ""),
        getattr(general_info.environmental_condition, "wind_speed", ""),
        getattr(general_info.environmental_condition, "seeing", ""),
        getattr(general_info.environmental_condition, "cloud_coverage", ""),
        getattr(general_info.environmental_condition, "moon_phase", ""),


        getattr(general_info.telescope_configuration, "air_mass", ""),
        getattr(general_info.telescope_configuration, "focus_position", ""),
        getattr(general_info.telescope_configuration, "tracking_mode", ""),
        getattr(general_info.telescope_configuration, "guiding_status", ""),
        getattr(general_info.telescope_configuration, "emergency_stop", ""),


        getattr(general_info.remote_operation, "remote_access", ""),
        getattr(general_info.remote_operation, "remote_observer", ""),

        getattr(general_info.comments, "comments", ""),
    ]

    
    headers = [
        "Session ID", "Telescope Name", "Operator", "Observer Name",
        "Log Start Time (UTC)", "Log Start Time (LST)", "Log End Time (UTC)", "Log End Time (LST)",
        "Target Name", "Right Ascension", "Declination", "Magnitude",
        "Instrument Name", "Observing Mode", "Exposure Time", "Calibration",
        "Filter In Use", "Polarization Mode", "Temprature", "Humidity",
        "Wind Speed", "Seeing", "Cloud Coverage", "Moon Phase",
        "Air Mass", "Focus Position", "Tracking Mode", "Guiding Status",
        "Emergency Stop", "Remote Access", "Remote Observer", "Comments"
    ]

    # Write to CSV
    write_header = not os.path.exists(csv_file_path)
    with open(csv_file_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow(headers)
        writer.writerow(row)