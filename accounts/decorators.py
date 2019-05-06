from django.views.decorators.csrf import csrf_exempt
from accounts.models import UserAuth
from api import settings
import jwt


def token_required(view):
    """
    this decorator checks whether request header has a valid jwt,
    if it has, the authenticated user is get and pointed at request object.
    """
    @csrf_exempt
    def wrap(request, *args, **kwargs):
        encoded_jwt = request.META.get('Authorization', request.META.get('HTTP_AUTHORIZATION', '')).split(' ')[-1]
        decoded_jwt = jwt.decode(encoded_jwt, key=settings.SECRET_KEY, leeway=30, algorithms=['HS256'])
        user_id = decoded_jwt.get('user_id')
        user = UserAuth.objects.get(uid=user_id)
        request.__dict__['authenticated_user'] = user
        return view(request, *args, **kwargs)
    return wrap
