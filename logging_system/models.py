from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# General Information
class GeneralInfo(models.Model):
    TELESCOPE_CHOICES = [
        ('TARA (1.2meter)','TARA (1.2meter)'),
        ('BHARMA (2.5meter)','BHARMA (2.5meter)')
    ]
    
    OBSERVATORY_CHOICES = [
        ('PRL Mount Abu Observatory','PRL Mount Abu Observatory')
    ]

    telescope_name = models.CharField(max_length=100, choices=TELESCOPE_CHOICES, default='TARA (1.2meter)')
    telescope_operator = models.CharField(max_length=100)
    observer_name = models.ForeignKey(User, on_delete=models.PROTECT)
    session_id = models.IntegerField(max_length=50, unique=True)
    log_start_time_lst = models.DateTimeField(blank=False, null=False, unique=True)
    log_start_time_utc = models.DateTimeField(blank=False, null=False)
    log_end_time_lst = models.DateTimeField(blank=False,  null=False, unique=True)
    log_end_time_utc = models.DateTimeField(blank=False, null=False)



# Environmental Conditions
class EnvironmentalCondition(models.Model):
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
    general_info = models.OneToOneField(
        GeneralInfo, 
        on_delete=models.CASCADE, 
        related_name='telescope_configuration'
    )

    TRACKING_MODES = [('Sidereal', 'Sidereal'), ('Lunar', 'Lunar'), ('Solar', 'Solar')]
    GUIDING_STATUSES = [('Active', 'Active'), ('Passive', 'Passive'), ('Disaled', 'Disabled')]

    focus_position = models.FloatField()
    air_mass = models.FloatField(default=0)
    tracking_mode = models.CharField(max_length=20, choices=TRACKING_MODES, default='Sidereal')
    guiding_status = models.CharField(max_length=20, choices=GUIDING_STATUSES, default='Active')
    emergency_stop = models.BooleanField(default=False)

# Instrumentation
class Instrumentation(models.Model):
    general_info = models.OneToOneField(
        GeneralInfo, 
        on_delete=models.CASCADE, 
        related_name='instrumentation'
    )

    OBSERVING_MODES = [('Imaging', 'Imaging'), ('Spectroscopy', 'Spectroscopy'), ('Spectropolarimetry', 'Spectropolarimetry'), ('Polarimetry', 'Polarimetry')]
    FILTERS = [('None', 'None'),('U', 'U'), ('B', 'B'), ('V', 'V'), ('R', 'R'), ('I', 'I')]
    INSTRUMENT_NAME = [('PARAS-1', 'PARAS-1'), ('PARAS-2', 'PARAS-2'), ('ProtoPol', 'ProtoPol'), ('LISA', 'LISA'),('EMPOL', 'EMPOL'),('LRS', 'LRS'),('FOSC', 'FOSC')]
    observing_mode = models.CharField(max_length=20, choices=OBSERVING_MODES, default='Imaging')
    instrument_name = models.CharField(max_length=100, choices=INSTRUMENT_NAME, default='PARAS-1')
    calibration = models.CharField(max_length=20, choices=[('Bias', 'Bias'), ('Dark', 'Dark'), ('Flat', 'Flat'), ('lamp', 'lamp')], default='Bias')
    filter_in_use = models.CharField(max_length=10, choices=FILTERS, default='U')
    exposure_time = models.FloatField(default='10')
    polarization_mode = models.BooleanField(default=False)

# Remote Operation and Network Status
class RemoteOperation(models.Model):
    general_info = models.OneToOneField(
        GeneralInfo, 
        on_delete=models.CASCADE, 
        related_name='remote_operation'
    )

    remote_access = models.BooleanField(default=False)
    remote_observer = models.CharField(max_length=100, blank=True, null=True)

class Comments(models.Model):
    general_info = models.OneToOneField(
        GeneralInfo, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )

    comments = models.TextField(blank=True, null=True)
