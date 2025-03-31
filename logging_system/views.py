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
from dotenv import load_dotenv

#required for downloading pdf
from bs4 import BeautifulSoup
from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
import pdfkit

#required for sending email
from django.core.mail import EmailMessage
from .forms import EmailForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

#required for fits file editing
import io
from astropy.io import fits
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

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
        email_form = EmailForm(request.POST)


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
            # Inject cleaned RA/Dec before saving 
            observation_instance.right_ascension = observation_form.cleaned_data['right_ascension']
            observation_instance.declination = observation_form.cleaned_data['declination']
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
                # Directly return the generated PDF file response.
                messages.success(request, 'Log Downloaded & Saved Successfully')
                return generate_pdf(request, general_instance.session_id)
            
            if 'send_email' in request.POST:
                recipient_list = [
                    "adityaradadiya294@gmail.com",
                    "adityaradadiya296@gmail.com",
                    request.user.email
                ]

                # Generate PDF for the saved log data
                pdf_path = create_pdf_file(general_instance.session_id)
                if not pdf_path:
                    messages.error(request, "Failed to generate PDF. Email not sent.")
                    return redirect('telescope_log')

                # Build the email body (similar to your session_detail email)
                email_body_html = f"""
                <html>
                <head></head>
                <body>
                    <p>Dear User,</p>
                    <p>Please find attached the telescope log report for session {general_instance.session_id}.</p>
                    <h3>Session Details:</h3>
                    <ul>
                        <li><strong>Session ID:</strong> {general_instance.session_id}</li>
                        <li><strong>Telescope:</strong> {general_instance.telescope_name}</li>
                        <li><strong>Operator:</strong> {general_instance.telescope_operator}</li>
                        <li><strong>Observer:</strong> {general_instance.observer_name}</li>
                        <li><strong>Log Start Time (UTC):</strong> {general_instance.log_start_time_utc.strftime('%Y-%m-%d %H:%M:%S')}</li>
                        <li><strong>Log Date:</strong> {general_instance.log_start_time_utc.strftime('%d %B %Y')}</li>
                        <li><strong>Instrument:</strong> {getattr(general_instance.instrumentation, 'instrument_name', 'N/A')}</li>
                        <li><strong>Exposure Time:</strong> {getattr(general_instance.instrumentation, 'exposure_time', 'N/A')} seconds</li>
                        <li><strong>Target Object:</strong> {getattr(general_instance.observation, 'target_name', 'N/A')}</li>
                    </ul>
                    <p>Best regards,<br>Telescope Logging System</p>
                </body>
                </html>
                """

                # Attempt to send the email
                try:
                    email_form = EmailForm(request.POST)
                    if email_form.is_valid():
                        additional_email = email_form.cleaned_data.get("recipient_email")
                        if additional_email:
                            email_list = [email.strip() for email in additional_email.split(",") if email.strip()]
                            for email in email_list:
                                try:
                                    validate_email(email)
                                except ValidationError:
                                    messages.error(request, f"Invalid email address: {email}")
                                    return redirect('telescope_log')
                            recipient_list.extend(email_list)
                    else:
                        messages.error(request, "Invalid email input.")
                        return redirect('telescope_log')
            
                    email = EmailMessage(
                        subject=f"{general_instance.telescope_name} Log - {general_instance.log_start_time_utc.strftime('%d %B %Y')}",
                        body=email_body_html,
                        from_email=os.getenv("EMAIL_HOST_USER"),
                        to=recipient_list
                        )
                    email.content_subtype = "html"
                    email.attach_file(pdf_path)
                    email.send()

                    messages.success(request, f"Log Saved & Email sent successfully to {', '.join(recipient_list)}.")
                    return redirect('telescope_log')
                except Exception as e:
                    messages.error(request, f"Failed to send email: {str(e)}")

                return redirect('telescope_log')

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
        email_form = EmailForm()

    return render(request, 'logging_system/telescope_log.html', {
        'general_form': general_form,
        'env_form': env_form,
        'telescope_form': telescope_form,
        'observation_form': observation_form,
        'instrumentation_form': instrumentation_form,
        'remote_form': remote_form,
        'comment_form': comment_form,
        'email_form': email_form,
        'session_id': locals().get('general_instance', None) and general_instance.session_id if 'send_email' in request.POST else None,
    })

def create_pdf_file(session_id):
    """Generate a PDF for a given session_id and return the file path."""
    wkhtmltopdf_path = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
    if not os.path.exists(wkhtmltopdf_path):
        return None

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
    full_html = render_to_string('logging_system/session_detail.html', context)
    soup = BeautifulSoup(full_html, "html.parser")
    tables = soup.find_all("table")
    table_titles = [
        "GENERAL INFORMATION", "WEATHER CONDITIONS", "OBSERVATION PARAMETERS",
        "TELESCOPE CONFIGURATION", "INSTRUMENTATION", "REMOTE OPERATION", "COMMENTS"
    ]
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
    table_html = f"<h2>Log Session: {session_id}</h2>{styles}<div class='container'>"
    for title, table in zip(table_titles, tables):
        table_html += f"<div class='table-box'><h3>{title}</h3>{str(table)}</div>"
    table_html += "</div>"

    pdf_options = {
    'page-size': 'A4',
    'orientation': 'Portrait',
    'encoding': 'UTF-8',
    'margin-top': '3mm',
    'margin-right': '5mm',
    'margin-bottom': '5mm',
    'margin-left': '5mm',
    'zoom': '0.5',  
    'viewport-size': '1920x1080',  
    'minimum-font-size': '6',  
    'dpi': 400,  
    'image-dpi': 100,  
    'disable-smart-shrinking': '',
    }
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    pdf_path = f"Log_{session_id}.pdf"
    pdfkit.from_string(table_html, pdf_path, options=pdf_options, configuration=config)
    return pdf_path

def generate_pdf(request, session_id):
    """Generate PDF and return it as a FileResponse for download."""
    pdf_path = create_pdf_file(session_id)
    if not pdf_path or not os.path.exists(pdf_path):
        return HttpResponse("Error generating PDF.", status=500)

    pdf_file = open(pdf_path, 'rb')
    response = FileResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Log_{session_id}.pdf"'
    return response
    
def send_email(request, session_id):
    """Send the generated PDF to a user-defined email."""
    general = get_object_or_404(GeneralInfo, session_id=session_id)
    recipient_list = [
        "adityaradadiya294@gmail.com",
        "adityaradadiya296@gmail.com",
        request.user.email
    ]

    

    pdf_path = create_pdf_file(session_id)
    if not pdf_path or not os.path.exists(pdf_path):
        messages.error(request, "Failed to generate PDF. Email not sent.")
        return redirect("session_detail", session_id=session_id)

    general = get_object_or_404(GeneralInfo, session_id=session_id)
    email_body_html = f"""
    <html>
    <head></head>
    <body>
        <p>Dear User,</p>
        <p>Please find attached the telescope log report for your session {general.session_id}.</p>
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
        </ul>
        <p>Best regards,<br>Telescope Logging System</p>
    </body>
    </html>
    """
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            additional_email = form.cleaned_data.get("recipient_email")
            if additional_email:
                email_list = [email.strip() for email in additional_email.split(",") if email.strip()]
                
                # Validate each email
                for email in email_list:
                    try:
                        validate_email(email)
                    except ValidationError:
                        messages.error(request, f"Invalid email address: {email}")
                        return redirect("session_detail", session_id=session_id)
                
                
                recipient_list.extend(email_list)

            try:
                email = EmailMessage(
                    subject=f"{general.telescope_name} Log - {general.log_start_time_utc.strftime('%d %B %Y')}",
                    body=email_body_html,
                    from_email=os.getenv("EMAIL_HOST_USER"),
                    to=recipient_list
                )
                email.content_subtype = "html"
                email.attach_file(pdf_path)
                email.send()

                messages.success(request, f"Email sent successfully to {', '.join(recipient_list)}.")
                return redirect("session_detail", session_id=session_id)
            except Exception as e:
                messages.error(request, f"Email sending failed: {str(e)}")
                return redirect("session_detail", session_id=session_id)
        else:
            messages.error(request, "Invalid email address provided.")

    else:
        form = EmailForm()

    # Render page again with the form and session details
    context = {
        "form": form,
        "general": general,
        "environmental_condition": getattr(general, "environmental_condition", None),
        "observation": getattr(general, "observation", None),
        "telescope_configuration": getattr(general, "telescope_configuration", None),
        "instrumentation": getattr(general, "instrumentation", None),
        "remote_operation": getattr(general, "remote_operation", None),
        "comments": getattr(general, "comments", None),
    }
    return render(request, "logging_system/session_detail.html", context)

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

@login_required
def fits_view(request):
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


    if request.method == "POST":
        form = FitsUploadForm(request.POST, request.FILES)
        session_id = request.POST.get("selected_log")

        if form.is_valid() and session_id:
            fits_file = request.FILES['fits_file']
            general = get_object_or_404(GeneralInfo, session_id=session_id)

            # Read and update FITS header
            with fits.open(fits_file) as hdul:
                header = hdul[0].header
                header['SESSION'] = general.session_id
                header['TELESCOP'] = general.telescope_name
                header['OBSERVER'] = str(general.observer_name)
                header['OPERATOR'] = general.telescope_operator
                header['TARGET'] = general.observation.target_name
                header['RA'] = general.observation.right_ascension
                header['DEC'] = general.observation.declination
                header['INSTRUME'] = general.instrumentation.instrument_name
                header['EXPTIME'] = general.instrumentation.exposure_time

                # Save new FITS file in buffer-memory
                updated_data = io.BytesIO()
                hdul.writeto(updated_data, overwrite=True)
                updated_data.seek(0)

                response = HttpResponse(updated_data.read(), content_type='application/fits')
                filename = f"Modified_{general.session_id}.fits"
                response['Content-Disposition'] = f'attachment; filename="{str(filename)}"'
                return response

        else:
            messages.error(request, "Invalid form submission or log not selected.")
    else:
        form = FitsUploadForm()

    return render(request, "logging_system/fits_page.html", {
        "form": form,
        "logs": logs,
    })