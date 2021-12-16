from django.contrib import admin
from .models import Patient, Appointment, Discharge

# Register your models here.
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Discharge)