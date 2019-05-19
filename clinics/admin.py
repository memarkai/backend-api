from django.contrib import admin

from clinics.models import ClinicUser


@admin.register(ClinicUser)
class ClinicUserAdmin(admin.ModelAdmin):
	exclude = ('password', )
	readonly_fields = ('created_at', )
	filter_horizontal = ('plans', )
