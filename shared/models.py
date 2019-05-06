import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class UniqueModel(models.Model):
	id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

	class Meta:
		abstract = True


class Specialty(UniqueModel):
	name = models.CharField(max_length=64)

	class Meta:
		verbose_name = _(u'Especialidade')
		verbose_name_plural = _(u'Especialidades')

	def __str__(self):
		return self.name


class HealthInsurance(UniqueModel):
	name = models.CharField(max_length=100)

	class Meta:
		verbose_name = _(u'Plano de saúde')
		verbose_name_plural = _(u'Planos de saúde')

	def __str__(self):
		return self.name
