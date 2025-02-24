
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import (
    GeneralInfoForm, EnvironmentalConditionForm, TelescopeConfigurationForm,
    ObservationForm, InstrumentationForm, RemoteOperationForm, CommentForm
)
from .models import GeneralInfo

# Create your views here.

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


            general_instance = general_form.save()
            
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

            return redirect('success')  # Redirect to a success page after saving

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

def success_view(request):
    return render(request, 'logging_system/success.html')

def log_data_view(request):

    query = request.GET.get('q')
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

    if query:
        logs = logs.filter( 
            Q(session_id__icontains=query) |
            Q(operator_name__icontains=query)
            )
    
    if date_filter:
        logs = logs.filter(log_start_time_utc__date=date_filter)

    context = {
        'logs': logs,
        'query': query,
        'date_filter': date_filter,
    }

    return render(request, 'logging_system/log_data.html', context)

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