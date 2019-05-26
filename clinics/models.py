from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from rest_framework import serializers
from shared.models import BaseProfile
import uuid

class Doctor(models.Model):
	crm_validator = RegexValidator(regex=r'^\d+?\/\w{2}$', message=_('Formato inválido'))
	
	id = models.UUIDField(primary_key=True, default=uuid.uuid4())
	name = models.CharField(max_length=200)
	crm = models.CharField(max_length=12, validators=[crm_validator])
	speciality = models.ForeignKey('shared.Specialty', on_delete=models.CASCADE)
	clinic = models.ForeignKey('clinics.ClinicUser', on_delete=models.CASCADE)

	class Meta:
		unique_together = ('crm', 'clinic',)

class DoctorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Doctor
		fields = '__all__'

class ClinicInsurance(models.Model):
	clinic = models.ForeignKey('clinics.ClinicUser', on_delete=models.CASCADE)
	plan = models.ForeignKey('shared.HealthInsurance', on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.clinic}: {self.plan}'

class ClinicUser(BaseProfile):
	plans = models.ManyToManyField('shared.HealthInsurance', related_name='clinics', through=ClinicInsurance)
	latitude = models.FloatField(null=True, validators=[MinValueValidator(0), MaxValueValidator(90)])
	longitude = models.FloatField(null=True, validators=[MinValueValidator(-180), MaxValueValidator(180)])

	class Meta:
		verbose_name = _(u'Clínica')
		verbose_name_plural = _(u'Clínicas')

	def list_doctors(self):
		return self.doctor_set.all()

class ClinicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicUser
        exclude = ('password', )
