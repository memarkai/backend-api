from django.db import models
from django.utils.translation import ugettext_lazy as _

from shared.models import BaseProfile


class PatientUser(BaseProfile):
	search_radius = models.PositiveSmallIntegerField(default=10, help_text=_(u'em km.'))
	insurance = models.ForeignKey('shared.HealthInsurance', on_delete=models.CASCADE, null=True, blank=True)

	class Meta:
		verbose_name = _(u'Paciente')
		verbose_name_plural = _(u'Pacientes')
