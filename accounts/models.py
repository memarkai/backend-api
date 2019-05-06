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

from shared.models import UniqueModel


class UserAuth(UniqueModel):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)

    class Meta:
        abstract = True

    @staticmethod
    def hash_it(msg):
        digest = hmac.new(str(settings.SECRET_KEY).encode(), msg=str(msg).encode(), digestmod=hashlib.sha256).digest()
        return base64.b64encode(digest).decode()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = UserAuth.hash_it(self.password)
        super(UserAuth, self).save(*args, **kwargs)

    @staticmethod
    def authenticate(email, password):
        user = UserAuth.objects.get(email=email)
        if UserAuth.hash_it(password) != user.password:
            raise PermissionDenied('Bad login or password')
        return jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=12),
        }, key=settings.SECRET_KEY, algorithm='HS256')

    def serialize(self):
        return vars(self)


class BaseProfile(UserAuth):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Formato inválido"))

    phone_number = models.CharField(validators=[phone_regex], max_length=17, null=True)
    phone = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
