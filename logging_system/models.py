
"""
Models for the Telescope Logging System.

Each model corresponds to a form section in the logging system and maps to a specific
category of telescope observation data:
- GeneralInfo: Main session data
- EnvironmentalCondition: Weather and atmosphere
- Observation: Target celestial object info
- TelescopeConfiguration: Equipment settings during session
- Instrumentation: Instrument use and exposure data
- RemoteOperation: Remote access configuration
- Comments: Optional user remarks

Each model links to `GeneralInfo` through a OneToOneField for structured session tracking.
"""

from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.

# General Information

def generate_session_id():
    return int(datetime.now().strftime("%Y%m%d%H%M%S"))

class GeneralInfo(models.Model):
    """
    Stores session-level general information about telescope observations.

    Attributes:
        telescope_name (str): Name of the telescope used.
        telescope_operator (str): Name of the person operating the telescope.
        observer_name (User): ForeignKey to the user observing the session.
        session_id (int): Unique identifier for the session.
        log_start_time_lst (datetime): Log start time in Local Sidereal Time.
        log_start_time_utc (datetime): Log start time in Coordinated Universal Time.
        log_end_time_lst (datetime): Log end time in Local Sidereal Time.
        log_end_time_utc (datetime): Log end time in Coordinated Universal Time.
    """

    TELESCOPE_CHOICES = [
        ('TARA (1.2meter)','TARA (1.2meter)'),
        ('BHARMA (2.5meter)','BHARMA (2.5meter)')
    ]
    

    telescope_name = models.CharField(max_length=100, choices=TELESCOPE_CHOICES, default='TARA (1.2meter)')
    telescope_operator = models.CharField(max_length=100)
    observer_name = models.ForeignKey(User, on_delete=models.PROTECT, default=1, null=True, blank=True)
    session_id = models.BigIntegerField(unique=True, default=generate_session_id)
    log_start_time_lst = models.DateTimeField(blank=False, null=False, unique=True)
    log_start_time_utc = models.DateTimeField(blank=False, null=False)
    log_end_time_lst = models.DateTimeField(blank=False,  null=False, unique=True)
    log_end_time_utc = models.DateTimeField(blank=False, null=False)



# Environmental Conditions
class EnvironmentalCondition(models.Model):

    """
    Stores atmospheric and environmental conditions during a session.

    Attributes:
        general_info (GeneralInfo): One-to-one relationship with GeneralInfo.
        temperature (float): Ambient temperature in degrees Celsius.
        humidity (float): Relative humidity percentage.
        wind_speed (float): Wind speed in m/s.
        seeing (float): Atmospheric seeing in arcseconds.
        cloud_coverage (str): Level of cloud coverage.
        moon_phase (str): Moon phase during the observation.
    """

    general_info = models.OneToOneField(
        GeneralInfo, 
        on_delete=models.CASCADE, 
        related_name='environmental_condition'
    )
    
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    seeing = models.FloatField()
    cloud_coverage = models.CharField(max_length=20)
    MOON_PHASES = [('New Moon', 'New Moon'), ('Full Moon', 'Full Moon'), ('First Quarter', 'First Quarter'), ('Last Quarter', 'Last Quarter')]
    moon_phase = models.CharField(max_length=20, choices=MOON_PHASES, default='New Moon')


# Observation Parameters
class Observation(models.Model):

    """
    Stores astronomical observation parameters for the session.

    Attributes:
        general_info (GeneralInfo): One-to-one relationship with GeneralInfo.
        target_name (str): Name of the target object.
        right_ascension (str): Right ascension of the target (HH:MM:SS).
        declination (str): Declination of the target (±DD:MM:SS).
        magnitude (str): Magnitude of the target object.
    """

    general_info = models.OneToOneField(
        GeneralInfo, 
        on_delete=models.CASCADE, 
        related_name='observation'
    )

    target_name = models.CharField(max_length=100)
    right_ascension = models.CharField(max_length=50)
    declination = models.CharField(max_length=50)
    magnitude = models.CharField(max_length=50)

# Telescope Configuration
class TelescopeConfiguration(models.Model):

    """
    Stores configuration details of the telescope during the session.

    Attributes:
        general_info (GeneralInfo): One-to-one relationship with GeneralInfo.
        focus_position (float): Focus position of the telescope.
        air_mass (float): Air mass at observation time.
        tracking_mode (str): Tracking mode (Sidereal, Lunar, Solar).
        guiding_status (str): Guiding status (Active, Passive, Disabled).
        emergency_stop (bool): Indicates whether emergency stop was activated.
    """

    general_info = models.OneToOneField(
        GeneralInfo, 
        on_delete=models.CASCADE, 
        related_name='telescope_configuration'
    )

    TRACKING_MODES = [('Sidereal', 'Sidereal'), ('Non-Sidreal','Non-Sidreal'), ('Lunar', 'Lunar')]
    GUIDING_STATUSES = [('Active', 'Active'), ('Passive', 'Passive'), ('Disaled', 'Disabled')]

    focus_position = models.FloatField()
    air_mass = models.FloatField(default=0)
    tracking_mode = models.CharField(max_length=20, choices=TRACKING_MODES, default='Sidereal')
    guiding_status = models.CharField(max_length=20, choices=GUIDING_STATUSES, default='Active')
    emergency_stop = models.BooleanField(default=False)

# Instrumentation
class Instrumentation(models.Model):

    """
    Stores instrumentation and observational setup details.

    Attributes:
        general_info (GeneralInfo): One-to-one relationship with GeneralInfo.
        observing_mode (str): Observing mode (e.g., Imaging, Spectroscopy).
        instrument_name (str): Name of the instrument used.
        calibration (str): Calibration method used.
        filter_in_use (str): Optical filter used during observation.
        exposure_time (float): Exposure time in seconds.
        polarization_mode (bool): Indicates if polarization mode was enabled.
    """

    general_info = models.OneToOneField(
        GeneralInfo, 
        on_delete=models.CASCADE, 
        related_name='instrumentation'
    )

    OBSERVING_MODES = [('Imaging', 'Imaging'), 
                       ('Spectroscopy', 'Spectroscopy'), 
                       ('Spectropolarimetry', 'Spectropolarimetry'), 
                       ('Polarimetry', 'Polarimetry')]
    FILTERS = [('None', 'None'),
               ('U', 'U'), 
               ('B', 'B'), 
               ('V', 'V'), 
               ('R', 'R'), 
               ('I', 'I'), 
               ('Enter Manually','Enter Manually')]
    INSTRUMENT_NAME = [('PARAS-1', 'PARAS-1'), 
                       ('PARAS-2', 'PARAS-2'), 
                       ('ProtoPol', 'ProtoPol'), 
                       ('LISA', 'LISA'),
                       ('EMPOL', 'EMPOL'),
                       ('LRS', 'LRS'),
                       ('FOSC', 'FOSC')]
    observing_mode = models.CharField(max_length=20, choices=OBSERVING_MODES, default='Imaging')
    instrument_name = models.CharField(max_length=100, choices=INSTRUMENT_NAME, default='PARAS-1')
    calibration = models.CharField(max_length=20, choices=[('Bias', 'Bias'), ('Sky','Sky'), ('Dark', 'Dark'), ('Flat', 'Flat'), ('lamp', 'lamp'), ('Not Applicable', 'Not Applicable')], default='Bias')
    filter_in_use = models.CharField(choices=FILTERS, default='U')
    exposure_time = models.FloatField(default='10')
    polarization_mode = models.BooleanField(default=False)


# Remote Operation and Network Status
class RemoteOperation(models.Model):

    """
    Stores remote operation details for the observation session.

    Attributes:
        general_info (GeneralInfo): One-to-one relationship with GeneralInfo.
        remote_access (bool): Indicates if remote access was enabled.
        remote_observer (str): Name of the remote observer (if any).
    """


    general_info = models.OneToOneField(
        GeneralInfo, 
        on_delete=models.CASCADE, 
        related_name='remote_operation'
    )

    remote_access = models.BooleanField(default=False)
    remote_observer = models.CharField(max_length=100, blank=True, null=True)

class Comments(models.Model):

    """
    Stores additional comments or notes related to the observation session.

    Attributes:
        general_info (GeneralInfo): One-to-one relationship with GeneralInfo.
        comments (str): Freeform comment text.
    """

    general_info = models.OneToOneField(
        GeneralInfo, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )

    comments = models.TextField(blank=True, null=True)
