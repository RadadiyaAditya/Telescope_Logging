from django.contrib import admin
from .models import GeneralInfo, EnvironmentalCondition, Observation, Instrumentation, RemoteOperation, Comments
# Register your models here.

admin.site.register(GeneralInfo)
admin.site.register(EnvironmentalCondition)
admin.site.register(Observation)
admin.site.register(Instrumentation)
admin.site.register(RemoteOperation)
admin.site.register(Comments)