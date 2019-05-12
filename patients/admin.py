from django.contrib import admin

from patients.models import PatientUser 


@admin.register(PatientUser)
class PatientUserAdmin(admin.ModelAdmin):
	exclude = ('password', )
	readonly_fields = ('created_at', )
