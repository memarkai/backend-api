from django.db import models
from clinics.models import ClinicUser, Doctor
from patients.models import PatientUser
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from .search import ConsultationIndex
import datetime
import uuid

def at_least_now(dt):
    if datetime.datetime.now() > dt:
        raise ValidationError(_(u'Não é possível agendar algo para o passado.'))

class Consultation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    clinic = models.ForeignKey(to=ClinicUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(to=Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(to=PatientUser, on_delete=models.CASCADE, null=True)
    candidates = models.ManyToManyField(to=PatientUser, related_name='candidates', null=True)
    start_date = models.DateTimeField(validators=[at_least_now])
    end_date = models.DateTimeField(validators=[at_least_now])

    def save(self, *args, **kwargs):
        if self.start_date > self.end_date:
            raise ValidationError(_(u'A data final da consulta deve ser maior do que a data inicial'))
        if (self.end_date - self.start_date).total_seconds() < 10 * 60:
            raise ValidationError(_(u'Uma consulta deve durar pelo menos dez minutos'))
        if self.doctor not in self.clinic.doctor_set.all():
            raise ValidationError(_(u'O médico informado não trabalha na clínica informada'))
        super(Consultation, self).save(*args, **kwargs)

    def indexing(self):
        obj = ConsultationIndex(
            meta={'id': self.id},
            clinic=self.clinic.id,
            clinic_location=[self.clinic.longitude, self.clinic.latitude],
            doctor=self.doctor.id,
            specialty=self.doctor.specialty.id,
            patient=self.patient.id if self.patient else None,
            candidates=[c.id for c in self.candidates.all()],
            start_date=self.start_date,
            end_date=self.end_date,
        )
        obj.save(index='consultation-index')
        return obj.to_dict(include_meta=True)


class ConsultationSerializer(serializers.BaseSerializer):
    class Meta:
        model = Consultation