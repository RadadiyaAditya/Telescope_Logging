"""
Forms for the Telescope Logging System.

Each form maps to a corresponding model or functional utility:
- GeneralInfoForm: Main session metadata (hidden + visible fields)
- EnvironmentalConditionForm: Atmospheric data inputs
- ObservationForm: Target object info, split RA/Dec
- TelescopeConfigurationForm: Setup for tracking, guiding, focus
- InstrumentationForm: Instrument and exposure setup
- RemoteOperationForm: Remote control session toggles
- CommentForm: Freeform remarks
- EmailForm: For sending PDFs via email
- FitsUploadForm: For FITS file metadata injection

All forms are compatible with crispy-forms and integrate Bootstrap classes.
"""


from django import forms
from .models import (
    GeneralInfo, EnvironmentalCondition, TelescopeConfiguration, 
    Observation, Instrumentation, RemoteOperation, Comments
)

# General Information Form
class GeneralInfoForm(forms.ModelForm):
    
    """
    Form for capturing general session-level observation metadata.

    Excludes:
        observer_name: This will be set automatically from the user session.

    Widgets:
        - log_start_time_utc, log_start_time_lst, log_end_time_utc, log_end_time_lst:
            Hidden inputs since they are populated automatically.
        - lst_time, utc_time:
            Displayed but readonly fields for LST/UTC time inputs.
    """

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
            'session_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            }
        
# Environmental Conditions Form
class EnvironmentalConditionForm(forms.ModelForm):

    """
    Form to input environmental conditions during the observation session.

    Excludes:
        general_info: Linked via relationship.

    Widgets:
        Form controls for temperature, humidity, wind, seeing, cloud coverage, and moon phase.
    """

    temperature = forms.DecimalField(
        label="Temperature (°C)",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.1",
            }
        ),
    )

    humidity = forms.DecimalField(
        label="Humidity (%)",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.1",
            }
        ),
    )

    wind_speed = forms.DecimalField(
        label="Wind Speed (km/s)",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.1",
            }
        ),
    )

    seeing = forms.DecimalField(
        label="Seeing (arcsec)",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.1",
            }
        ),
    )



    class Meta:
        model = EnvironmentalCondition
        fields = '__all__'
        exclude = ['general_info']
        widgets = {
            'cloud_coverage': forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Cloud Coverage",
                }
            ),
            'moon_phase': forms.Select(
                attrs={
                    "class": "form-select",
                    "placeholder": "Moon Phase",
                }
            ),
        }


# Observation Form
class ObservationForm(forms.ModelForm):

    """
    Form for recording observational target parameters including RA/Dec fields.

    Custom Fields:
        - RA (hour, minute, second): Input split for RA.
        - Dec (degree, minute, second): Input split for Declination.

    Excludes:
        - general_info: Linked via relationship. 
        - right_ascension, declination: Combined from subfields.

    Methods:
        clean(): Combines individual RA/Dec fields into formatted strings.
    """

    ra_hour = forms.IntegerField(label="RA Hours", min_value=0, max_value=23, widget=forms.NumberInput(attrs={'placeholder': 'HH', 'class': 'form-control'}))
    ra_minute = forms.IntegerField(label="RA Minutes", min_value=0, max_value=59, widget=forms.NumberInput(attrs={'placeholder': 'MM', 'class': 'form-control'}))
    ra_second = forms.DecimalField(label="RA Seconds", min_value=0, max_value=59.999, decimal_places=2, widget=forms.NumberInput(attrs={'placeholder': 'SS.ss', 'class': 'form-control'}))

    dec_degree = forms.IntegerField(label="Dec Degrees", min_value=-90, max_value=90, widget=forms.NumberInput(attrs={'placeholder': 'DD', 'class': 'form-control'}))
    dec_minute = forms.IntegerField(label="Dec Minutes", min_value=0, max_value=59, widget=forms.NumberInput(attrs={'placeholder': 'MM', 'class': 'form-control'}))
    dec_second = forms.DecimalField(label="Dec Seconds", min_value=0, max_value=59.999, decimal_places=2, widget=forms.NumberInput(attrs={'placeholder': 'SS.ss', 'class': 'form-control'}))
    class Meta:
        model = Observation
        fields = '__all__'
        exclude = ['general_info', 'right_ascension', 'declination']
        widgets = {
            'magnitude': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'eg. V=67.8'}),
        }

    target_name = forms.CharField(
        label="Target name (as per SIMBAD)",
        widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'eg. NGC 1234'}),
    )


    def clean(self):
        """
        Validates and combines RA and Dec inputs into single formatted strings.

        Returns:
            dict: Cleaned data with added right_ascension and declination fields.

        Raises:
            forms.ValidationError: If RA/Dec components are missing or invalid.
        """

        cleaned_data = super().clean()

        try:
            ra = f"{cleaned_data['ra_hour']:02} {cleaned_data['ra_minute']:02} {cleaned_data['ra_second']:05.2f}"
            dec = f"{cleaned_data['dec_degree']:02} {cleaned_data['dec_minute']:02} {cleaned_data['dec_second']:05.2f}"
            cleaned_data['right_ascension'] = ra
            cleaned_data['declination'] = dec
        except KeyError:
            raise forms.ValidationError("Invalid RA/Dec format.")
        return cleaned_data


# Telescope Configuration Form
class TelescopeConfigurationForm(forms.ModelForm):
    """
    Form for configuring telescope hardware settings.

    Excludes:
        general_info: Linked via relationship.

    Widgets:
        Numeric inputs for pointing accuracy and focus position.
    """

    class Meta:
        model = TelescopeConfiguration
        fields = '__all__'
        exclude = ['general_info']
        widgets = {
            'focus_position': forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control', 'placeholder': 'Focus Position'}),
        }


# Instrumentation Form
class InstrumentationForm(forms.ModelForm):

    """
    Form for specifying instrument settings and exposure configurations.

    Excludes:
        general_info: Linked via relationship.

    Fields:
        exposure_time: Float input with step control.
    """
    FILTERS = [
        ('None', 'None'),
        ('U', 'U'),
        ('B', 'B'),
        ('V', 'V'),
        ('R', 'R'),
        ('I', 'I'),
        ('Enter Manually', 'Enter Manually')
    ]

    filter_in_use = forms.ChoiceField(
        choices=FILTERS,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_filter_dropdown'})
    )

    custom_filter = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter filter name',
            'id': 'id_custom_filter',
            'style': 'display:none;'
        })
    )

    class Meta:
        model = Instrumentation
        fields = '__all__'
        exclude = ['general_info']

    exposure_time = forms.FloatField(
        label="Exposure Time (sec)",
        widget=forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control', 'placeholder': 'eg. 200s'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        filter_choice = cleaned_data.get('filter_in_use')
        custom = cleaned_data.get('custom_filter')

        if filter_choice == 'Enter Manually' and not custom:
            raise forms.ValidationError("Please enter a custom filter value.")
        return cleaned_data

# Remote Operation Form
class RemoteOperationForm(forms.ModelForm):

    """
    Form to manage and record remote observation capabilities.

    Excludes:
        general_info: Linked via relationship.

    Fields:
        remote_access: Radio button selection for Yes/No.
    """

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

    """
    Form for adding optional comments related to the session.

    Excludes:
        general_info: Linked via relationship.

    Widgets:
        Multiline textarea for user comments.
    """

    class Meta:
        model = Comments
        fields = '__all__'
        exclude = ['general_info']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'placeholder': 'Enter comments here...'}),
        }

class EmailForm(forms.Form):

    """
    Simple form for entering recipient email addresses for email functionality.

    Fields:
        recipient_email (str): Comma-separated list of email addresses.
    """

    recipient_email = forms.CharField(required=False, 
                                       help_text="If you want to send mail to multiple addresses, separate emails with commas.",  
                                       widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "example1@gmail.com, example2@gmail.com"}))
