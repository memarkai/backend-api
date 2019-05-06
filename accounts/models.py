import base64
import datetime
import hashlib
import hmac
import jwt
import uuid

from django.db import models
from django.conf import settings

from rest_framework.exceptions import PermissionDenied


class UserAuth(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
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
            self.id = uuid.uuid4()
            self.password = UserAuth.hash_it(self.password)
        super(UserAuth, self).save(*args, **kwargs)

    @staticmethod
    def authenticate(email, password):
        user = UserAuth.objects.get(email=email)
        if UserAuth.hash_it(password) != user.password:
            raise PermissionDenied('Bad login or password')
        return jwt.encode({
            'user_id': user.uid,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=12),
        }, key=settings.SECRET_KEY, algorithm='HS256')

    def serialize(self):
        return vars(self)
