# Generated by Django 5.1.7 on 2025-05-04 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logging_system', '0002_alter_generalinfo_observer_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environmentalcondition',
            name='cloud_coverage',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='environmentalcondition',
            name='humidity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='environmentalcondition',
            name='moon_phase',
            field=models.CharField(blank=True, choices=[('New Moon', 'New Moon'), ('Full Moon', 'Full Moon'), ('First Quarter', 'First Quarter'), ('Last Quarter', 'Last Quarter')], default=None, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='environmentalcondition',
            name='seeing',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='environmentalcondition',
            name='temperature',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='environmentalcondition',
            name='wind_speed',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='generalinfo',
            name='log_end_time_lst',
            field=models.DateTimeField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='generalinfo',
            name='log_end_time_utc',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='generalinfo',
            name='log_start_time_lst',
            field=models.DateTimeField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='generalinfo',
            name='log_start_time_utc',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='generalinfo',
            name='telescope_name',
            field=models.CharField(choices=[('TARA (1.2meter)', 'TARA (1.2meter)'), ('BHARMA (2.5meter)', 'BHARMA (2.5meter)')], default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='generalinfo',
            name='telescope_operator',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='instrumentation',
            name='calibration',
            field=models.CharField(blank=True, choices=[('Bias', 'Bias'), ('Sky', 'Sky'), ('Dark', 'Dark'), ('Flat', 'Flat'), ('lamp', 'lamp'), ('Not Applicable', 'Not Applicable')], default=None, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='instrumentation',
            name='exposure_time',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='instrumentation',
            name='filter_in_use',
            field=models.CharField(blank=True, choices=[('None', 'None'), ('U', 'U'), ('B', 'B'), ('V', 'V'), ('R', 'R'), ('I', 'I'), ('Enter Manually', 'Enter Manually')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='instrumentation',
            name='instrument_name',
            field=models.CharField(blank=True, choices=[('PARAS-1', 'PARAS-1'), ('PARAS-2', 'PARAS-2'), ('ProtoPol', 'ProtoPol'), ('LISA', 'LISA'), ('EMPOL', 'EMPOL'), ('LRS', 'LRS'), ('FOSC', 'FOSC')], default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='instrumentation',
            name='observing_mode',
            field=models.CharField(blank=True, choices=[('Imaging', 'Imaging'), ('Spectroscopy', 'Spectroscopy'), ('Spectropolarimetry', 'Spectropolarimetry'), ('Polarimetry', 'Polarimetry')], default=None, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='instrumentation',
            name='polarization_mode',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='observation',
            name='declination',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='observation',
            name='magnitude',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='observation',
            name='right_ascension',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='observation',
            name='target_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='remoteoperation',
            name='remote_access',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='telescopeconfiguration',
            name='air_mass',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='telescopeconfiguration',
            name='focus_position',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='telescopeconfiguration',
            name='guiding_status',
            field=models.CharField(blank=True, choices=[('Active', 'Active'), ('Passive', 'Passive'), ('Disaled', 'Disabled')], default=None, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='telescopeconfiguration',
            name='tracking_mode',
            field=models.CharField(blank=True, choices=[('Sidereal', 'Sidereal'), ('Non-Sidreal', 'Non-Sidreal'), ('Lunar', 'Lunar')], default=None, max_length=20, null=True),
        ),
    ]
