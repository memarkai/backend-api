import jwt

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status


def token_required(model):

    def true_decorator(func):

        @csrf_exempt
        def wrap(request, *args, **kwargs):
            encoded_jwt = request.META.get('Authorization', request.META.get('HTTP_AUTHORIZATION', '')).split(' ')[-1]
            decoded_jwt = jwt.decode(encoded_jwt, key=settings.SECRET_KEY, leeway=30, algorithms=['HS256'])
            user_id = decoded_jwt.get('user_id')
            try:
                user = model.objects.get(uid=user_id)
            except model.DoesNotExist:
                return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)
            request.__dict__['authenticated_user'] = user
            return func(request, *args, **kwargs)
        
        return wrap
    true_decorator.__name__ = f'{model.__name__.lower()}_token_required'

    return true_decorator
