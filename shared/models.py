import base64
import datetime
import hashlib
import hmac
import jwt
import uuid
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import PermissionDenied
from rest_framework import serializers


class BaseProfile(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Formato inválido"))
    phone = models.CharField(validators=[phone_regex], max_length=17, null=True)
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    image = models.FileField(upload_to='images/', null=True, verbose_name="")


    is_staff = models.BooleanField(default=False)

    @staticmethod
    def hash_it(msg):
        digest = hmac.new(str(settings.SECRET_KEY).encode(), msg=str(msg).encode(), digestmod=hashlib.sha256).digest()
        return base64.b64encode(digest).decode()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = BaseProfile.hash_it(self.password)
            self.id = uuid.uuid4()
        super(BaseProfile, self).save(*args, **kwargs)

    @classmethod
    def authenticate(cls, email, password):
        user = cls.objects.get(email=email)
        if cls.hash_it(password) != user.password:
            raise PermissionDenied('Bad login or password')
        return jwt.encode({
            'user_id': str(user.id),
        }, key=settings.SECRET_KEY, algorithm='HS256')

    def __str__(self):
        return self.email

class Specialty(models.Model):
	id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
	name = models.CharField(max_length=64)

	class Meta:
		verbose_name = _(u'Especialidade')
		verbose_name_plural = _(u'Especialidades')

	def __str__(self):
		return self.name

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = '__all__'


class HealthInsurance(models.Model):
	id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
	name = models.CharField(max_length=100)

	class Meta:
		verbose_name = _(u'Plano de saúde')
		verbose_name_plural = _(u'Planos de saúde')

	def __str__(self):
		return self.name

class HealthInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthInsurance
        fields = '__all__'
