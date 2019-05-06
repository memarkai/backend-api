import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class UniqueModel(models.Model):
	id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

	class Meta:
		abstract = True


class Specialty(UniqueModel):
	name = models.CharField(max_length=64)

	def __str__(self):
		return self.name
