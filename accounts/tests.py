from django.test import TestCase
from accounts.models import UserAuth
import uuid
import random
import string


class UserAuthTests(TestCase):

    def test_password_is_being_hashed(self):
        str_password = uuid.uuid4().hex
        email = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(10, 20))) + '@test.com'
        user = UserAuth(email=email, password=str_password)
        user.save()
        user_again = UserAuth.objects.get(email=email)
        self.assertNotEqual(str_password, user_again.password)
