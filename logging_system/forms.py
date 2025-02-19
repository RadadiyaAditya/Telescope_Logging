from django import forms
from .models import (
    GeneralInfo, EnvironmentalCondition, TelescopeConfiguration, 
    Observation, Instrumentation, RemoteOperation, Comments
)

# General Information Form
class GeneralInfoForm(forms.ModelForm):
    class Meta:
        model = GeneralInfo
        fields = '__all__'
        widgets = {
            'log_start_time_utc': forms.HiddenInput(),
            'log_start_time_lst': forms.HiddenInput(),
            'log_end_time_utc': forms.HiddenInput(),
            'log_end_time_lst': forms.HiddenInput(),
            'lst_time': forms.DateTimeInput(attrs={'readonly': 'readonly', 'type': 'datetime-local'}),
            'utc_time': forms.DateTimeInput(attrs={'readonly': 'readonly', 'type': 'datetime-local'}),
            }
# Environmental Conditions Form
class EnvironmentalConditionForm(forms.ModelForm):
    class Meta:
        model = EnvironmentalCondition
        fields = '__all__'
        widgets = {
            'temperature': forms.NumberInput(attrs={'step': '0.1'}),
            'humidity': forms.NumberInput(attrs={'step': '0.1'}),
            'wind_speed': forms.NumberInput(attrs={'step': '0.1'}),
            'seeing': forms.NumberInput(attrs={'step': '0.1'}),
        }

# Observation Form
class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = '__all__'

    target_name = forms.CharField(
        label="Target name (as per SIMBAD)",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )


# Telescope Configuration Form
class TelescopeConfigurationForm(forms.ModelForm):
    class Meta:
        model = TelescopeConfiguration
        fields = '__all__'
        widgets = {
            'pointing_accuracy': forms.NumberInput(attrs={'step': '0.1'}),
            'focus_position': forms.NumberInput(attrs={'step': '0.1'}),
        }


# Instrumentation Form
class InstrumentationForm(forms.ModelForm):
    class Meta:
        model = Instrumentation
        fields = '__all__'
        widgets = {
            'exposure_time': forms.NumberInput(attrs={'step': '0.1'}),
        }

# Remote Operation Form
class RemoteOperationForm(forms.ModelForm):
    class Meta:
        model = RemoteOperation
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = '__all__'
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'placeholder': 'Enter comments here...'}),
        }
