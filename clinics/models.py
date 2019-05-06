from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.models import BaseProfile


class ClinicSpecialty(models.Model):
	clinic = models.ForeignKey('clinics.ClinicUser', on_delete=models.CASCADE)
	specialty = models.ForeignKey('shared.Specialty', on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.clinic}: {self.specialty}'


class ClinicInsurance(models.Model):
	clinic = models.ForeignKey('clinics.ClinicUser', on_delete=models.CASCADE)
	plan = models.ForeignKey('shared.HealthInsurance', on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.clinic}: {self.plan}'


class ClinicUser(BaseProfile):
	specialties = models.ManyToManyField('shared.Specialty', related_name='clinics', through=ClinicSpecialty)
	plans = models.ManyToManyField('shared.HealthInsurance', related_name='clinics', through=ClinicInsurance)

	class Meta:
		verbose_name = _(u'Clínica')
		verbose_name_plural = _(u'Clínicas')
