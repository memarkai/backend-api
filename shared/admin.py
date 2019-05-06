from django.contrib import admin

from shared.models import Specialty, HealthInsurance

admin.site.register([Specialty, HealthInsurance])
