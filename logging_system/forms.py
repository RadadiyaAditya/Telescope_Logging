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
            # these parameters are in database but will be hidden on webapp
            'log_start_time_utc': forms.HiddenInput(),
            'log_start_time_lst': forms.HiddenInput(),
            'log_end_time_utc': forms.HiddenInput(),
            'log_end_time_lst': forms.HiddenInput(),

            # these parameters are not in databse but will be shown on webapp
            'lst_time': forms.DateTimeInput(attrs={'readonly': 'readonly', 'type': 'datetime-local'}),
            'utc_time': forms.DateTimeInput(attrs={'readonly': 'readonly', 'type': 'datetime-local'}),
            }
# Environmental Conditions Form
class EnvironmentalConditionForm(forms.ModelForm):
    class Meta:
        model = EnvironmentalCondition
        fields = '__all__'
        exclude = ['general_info']
        widgets = {
            'humidity': forms.NumberInput(attrs={'step': '0.1'}),
            'wind_speed': forms.NumberInput(attrs={'step': '0.1'}),
            'seeing': forms.NumberInput(attrs={'step': '0.1'}),
        }
    temperature = forms.FloatField(
        label="Temprature (°C)",
        widget=forms.NumberInput(attrs={'step': '0.1'}),
    )
    humidity = forms.FloatField(
        label="Humidity (%)",
        widget=forms.NumberInput(attrs={'step': '0.1'}),
    )
    wind_speed = forms.FloatField(
        label="Wind Speed (m/s)",
        widget=forms.NumberInput(attrs={'step': '0.1'}),
    )
    cloud_cover = forms.FloatField(
        label="Cloud Cover (%)",
        widget=forms.NumberInput(attrs={'step': '0.1'}),
    )
    seeing = forms.FloatField(
        label="Seeing (arcsec)",
        widget=forms.NumberInput(attrs={'step': '0.1'}),
    )
# Observation Form
class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = '__all__'
        exclude = ['general_info']

    target_name = forms.CharField(
        label="Target name (as per SIMBAD)",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    right_ascension = forms.TimeField(
        label="Right Ascension (hh:mm:ss)",
        widget=forms.TimeInput(attrs={"class": "form-control"}),
    )
    declination = forms.CharField(
        label="Declination (dd:mm:ss)",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )  


# Telescope Configuration Form
class TelescopeConfigurationForm(forms.ModelForm):
    class Meta:
        model = TelescopeConfiguration
        fields = '__all__'
        exclude = ['general_info']
        widgets = {
            'pointing_accuracy': forms.NumberInput(attrs={'step': '0.1'}),
            'focus_position': forms.NumberInput(attrs={'step': '0.1'}),
        }


# Instrumentation Form
class InstrumentationForm(forms.ModelForm):
    class Meta:
        model = Instrumentation
        fields = '__all__'
        exclude = ['general_info']

    exposure_time = forms.FloatField(
        label="Exposure Time (sec)",
        widget=forms.NumberInput(attrs={'step': '0.1'}),
    )

# Remote Operation Form
class RemoteOperationForm(forms.ModelForm):
    class Meta:
        model = RemoteOperation
        fields = '__all__'
        exclude = ['general_info']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = '__all__'
        exclude = ['general_info']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'placeholder': 'Enter comments here...'}),
        }
