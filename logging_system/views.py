
from django.shortcuts import render, redirect
from .forms import (
    GeneralInfoForm, EnvironmentalConditionForm, TelescopeConfigurationForm,
    ObservationForm, InstrumentationForm, RemoteOperationForm, CommentForm
)
from datetime import datetime, timezone
from .lst import compute_lst
# Create your views here.

def telescope_log_view(request):
    lst_time = compute_lst(datetime.now())  # Compute LST time
    utc_time = datetime.now(timezone.utc)  # Get UTC time

    if request.method == 'POST':
        general_form = GeneralInfoForm(request.POST)
        env_form = EnvironmentalConditionForm(request.POST)
        telescope_form = TelescopeConfigurationForm(request.POST)
        observation_form = ObservationForm(request.POST)
        instrumentation_form = InstrumentationForm(request.POST)
        remote_form = RemoteOperationForm(request.POST)
        comment_form = CommentForm(request.POST)

        if 'start_log' in request.POST:
            general_form.data['log_start_time_lst'] = lst_time
            general_form.data['log_start_time_utc'] = utc_time

        if 'end_log' in request.POST:
            general_form.data['log_end_time_lst'] = lst_time
            general_form.data['log_end_time_utc'] = utc_time


        else:
            general_form = GeneralInfoForm()

        if (general_form.is_valid() and env_form.is_valid() and telescope_form.is_valid() and
            observation_form.is_valid() and instrumentation_form.is_valid() and remote_form.is_valid() and
            comment_form.is_valid()):

            general_form.save()
            env_form.save()
            telescope_form.save()
            observation_form.save()
            instrumentation_form.save()
            remote_form.save()
            comment_form.save()

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
        'lst_time': lst_time,
        'utc_time': utc_time,
        'env_form': env_form,
        'telescope_form': telescope_form,
        'observation_form': observation_form,
        'instrumentation_form': instrumentation_form,
        'remote_form': remote_form,
        'comment_form': comment_form,
    })

def success_view(request):
    return render(request, 'logging_system/success.html')

