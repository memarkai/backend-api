from django.db import models
import hmac
import hashlib
import base64
from api import settings
from rest_framework.exceptions import PermissionDenied
import datetime
import jwt
# Create your models here.


class UserAuth(models.Model):
    uid = models.UUIDField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)

    @staticmethod
    def hash_it(msg):
        digest = hmac.new(settings.SECRET_KEY, msg=msg, digestmod=hashlib.sha256).digest()
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
            'user_id': user.uid,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=12),
        }, key=settings.SECRET_KEY, algorithm='HS256')

    def serialize(self):
        return vars(self)
