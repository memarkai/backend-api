from django.db import models
import hmac
import hashlib
import base64
from api import settings
# Create your models here.


class UserAuth(models.Model):
    uuid = models.UUIDField(primary_key=True)
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

    def serialize(self):
        return vars(self)
