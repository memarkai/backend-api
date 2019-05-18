from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from shared.models import BaseProfile

class Doctor(models.Model):
	crm_validator = RegexValidator(regex=r'^\d+?\/\w{2}$', message=_('Formato inválido'))
	name = models.CharField(max_length=200)
	crm = models.CharField(max_length=12, primary_key=True, validators=[crm_validator])
	speciality = models.ForeignKey('shared.Specialty', on_delete=models.CASCADE)
	

class ClinicDoctor(models.Model):
	clinic = models.ForeignKey('clinics.ClinicUser', on_delete=models.CASCADE)
	doctor = models.ForeignKey('clinics.Doctor', on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.clinic}: {self.specialty}'


class ClinicInsurance(models.Model):
	clinic = models.ForeignKey('clinics.ClinicUser', on_delete=models.CASCADE)
	plan = models.ForeignKey('shared.HealthInsurance', on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.clinic}: {self.plan}'


class ClinicUser(BaseProfile):
	doctors = models.ManyToManyField('clinics.Doctor', related_name='clinics', through=ClinicDoctor)
	plans = models.ManyToManyField('shared.HealthInsurance', related_name='clinics', through=ClinicInsurance)

	class Meta:
		verbose_name = _(u'Clínica')
		verbose_name_plural = _(u'Clínicas')
