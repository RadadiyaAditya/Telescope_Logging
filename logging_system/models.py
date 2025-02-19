from django.db import models

# Create your models here.


class GeneralInfo(models.Model):
    TELESCOPE_CHOICES = [
        ('TARA (1.2mm)','TARA (1.2mm)'),
        ('BHARMA (2.5mm)','BHARMA (2.5mm)')
    ]
    
    OBSERVATORY_CHOICES = [
        ('PRL Mount Abu Observatory','PRL Mount Abu Observatory')
    ]
    
    telescope_name = models.CharField(max_length=100, choices=TELESCOPE_CHOICES)
    observatory_name = models.CharField(max_length=100, choices=OBSERVATORY_CHOICES)
    operator_name = models.CharField(max_length=100)
    session_id = models.CharField(max_length=50)
    log_start_time_lst = models.DateTimeField(blank=True, null=True)
    log_start_time_utc = models.DateTimeField(blank=True, null=True)
    log_end_time_lst = models.DateTimeField(blank=True, null=True)
    log_end_time_utc = models.DateTimeField(blank=True, null=True)


# Environmental Conditions
class EnvironmentalCondition(models.Model):
    TEMPERATURE_UNITS = [('C', 'Celsius'), ('K', 'Kelvin')]
    
    temperature = models.FloatField()
    temperature_unit = models.CharField(max_length=1, choices=TEMPERATURE_UNITS, default='C')
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    seeing = models.FloatField()
    cloud_cover = models.FloatField()
    MOON_PHASES = [('New Moon', 'New Moon'), ('Full Moon', 'Full Moon'), ('First Quarter', 'First Quarter'), ('Last Quarter', 'Last Quarter')]
    moon_phase = models.CharField(max_length=20, choices=MOON_PHASES, default='New Moon')


# Observation Parameters
class Observation(models.Model):
    target_name = models.CharField(max_length=100)
    right_ascension = models.CharField(max_length=50)
    declination = models.CharField(max_length=50)
    air_mass = models.FloatField()
    magnitude = models.FloatField(null=True, blank=True)

# Telescope Configuration
class TelescopeConfiguration(models.Model):
    TRACKING_MODES = [('Sidereal', 'Sidereal'), ('Lunar', 'Lunar'), ('Solar', 'Solar')]
    GUIDING_STATUSES = [('Active', 'Active'), ('Passive', 'Passive'), ('Disaled', 'Disabled')]

    focus_position = models.FloatField()
    tracking_mode = models.CharField(max_length=20, choices=TRACKING_MODES, default='Sidereal')
    guiding_status = models.CharField(max_length=20, choices=GUIDING_STATUSES, default='Active')

# Instrumentation
class Instrumentation(models.Model):
    OBSERVING_MODES = [('Imaging', 'Imaging'), ('Spectroscopy', 'Spectroscopy'), ('Spectropolarimetry', 'Spectropolarimetry'), ('Polarimetry', 'Polarimetry')]
    FILTERS = [('U', 'U'), ('B', 'B'), ('V', 'V'), ('R', 'R'), ('I', 'I')]

    observing_mode = models.CharField(max_length=20, choices=OBSERVING_MODES, default='Imaging')
    instrument_name = models.CharField(max_length=100)
    filter_in_use = models.CharField(max_length=10, choices=FILTERS, default='U')
    exposure_time = models.FloatField()
    polarization_mode = models.BooleanField(default=True)

# Remote Operation and Network Status
class RemoteOperation(models.Model):
    remote_access = models.BooleanField(default=False)
    remote_observer = models.CharField(max_length=100, blank=True, null=True)
    emergency_stop = models.BooleanField(default=False)

class Comments(models.Model):
    comments = models.TextField(blank=True, null=True)
