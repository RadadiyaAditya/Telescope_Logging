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
        exclude = ['observer_name']
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
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'humidity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'wind_speed': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'seeing': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'cloud_coverage': forms.TextInput(attrs={'class': 'form-control'}),
            'moon_phase': forms.Select(attrs={'class': 'form-control'}),
        }
# Observation Form
class ObservationForm(forms.ModelForm):

    ra_hour = forms.IntegerField(label="RA Hours", min_value=0, max_value=23, widget=forms.NumberInput(attrs={'placeholder': 'HH', 'class': 'form-control'}))
    ra_minute = forms.IntegerField(label="RA Minutes", min_value=0, max_value=59, widget=forms.NumberInput(attrs={'placeholder': 'MM', 'class': 'form-control'}))
    ra_second = forms.DecimalField(label="RA Seconds", min_value=0, max_value=59.999, decimal_places=2, widget=forms.NumberInput(attrs={'placeholder': 'SS.ss', 'class': 'form-control'}))
 
    dec_sign = forms.ChoiceField(label="Declination Sign", choices=[('+', '+'), ('-', '-')], widget=forms.Select(attrs={'class': 'form-control'}))
    dec_degree = forms.IntegerField(label="Dec Degrees", min_value=0, max_value=90, widget=forms.NumberInput(attrs={'placeholder': 'DD', 'class': 'form-control'}))
    dec_minute = forms.IntegerField(label="Dec Minutes", min_value=0, max_value=59, widget=forms.NumberInput(attrs={'placeholder': 'MM', 'class': 'form-control'}))
    dec_second = forms.DecimalField(label="Dec Seconds", min_value=0, max_value=59.999, decimal_places=2, widget=forms.NumberInput(attrs={'placeholder': 'SS.ss', 'class': 'form-control'}))
    class Meta:
        model = Observation
        fields = '__all__'
        exclude = ['general_info', 'right_ascension', 'declination']

    target_name = forms.CharField(
        label="Target name (as per SIMBAD)",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )


    def clean(self):
        cleaned_data = super().clean()

        try:
            ra = f"{cleaned_data['ra_hour']:02} {cleaned_data['ra_minute']:02} {cleaned_data['ra_second']:05.2f}"
            dec = f"{cleaned_data['dec_sign']}{cleaned_data['dec_degree']:02} {cleaned_data['dec_minute']:02} {cleaned_data['dec_second']:05.2f}"
            cleaned_data['right_ascension'] = ra
            cleaned_data['declination'] = dec
        except KeyError:
            raise forms.ValidationError("Invalid RA/Dec format.")
        return cleaned_data


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
    REMOTE_ACCESS_CHOICES = (
        (True, 'Yes'),
        (False, 'No'),
    )

    remote_access = forms.ChoiceField(
        label="Remote Access",
        choices=REMOTE_ACCESS_CHOICES,
        widget=forms.RadioSelect,
    )
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

class EmailForm(forms.Form):
    recipient_email = forms.CharField(required=False, 
                                       help_text="If you want to send mail to multiple addresses, separate emails with commas.",  
                                       widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "example1@gmail.com, example2@gmail.com"}))

class FitsUploadForm(forms.Form):
    fits_file = forms.FileField(label="Upload FITS File")