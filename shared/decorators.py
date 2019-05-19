import jwt
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from .models import BaseProfile
from clinics.models import ClinicUser
from patients.models import PatientUser
from django.utils.translation import ugettext_lazy as _

class IsClinic(permissions.BasePermission):
    message = _('You are not a clinic')

    def has_permission(self, request, view):
        try:
            clinic = ClinicUser.objects.get(id=request.user.id)
            request.user.__dict__['clinic'] = clinic
        except ObjectDoesNotExist:
            return False
        else:
            return True

class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'patient')

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user)
        print(obj)
        print(obj.user)
        return True

class IsTokenAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            encoded_jwt = request.META.get('Authorization', request.META.get('HTTP_AUTHORIZATION', '')).split(' ')[-1]
            decoded_jwt = jwt.decode(encoded_jwt, key=settings.SECRET_KEY, leeway=30, algorithms=['HS256'])
            user_id = decoded_jwt.get('user_id')
            user = BaseProfile.objects.get(id=user_id)
            request.user = user
            request.user.__dict__['is_authenticated'] = True
        except jwt.ExpiredSignature:
            return False
        except ObjectDoesNotExist:
            return False
        else:
            return True

# def token_required(view):
#     """
#     this decorator checks whether request header has a valid jwt,
#     if it has, the authenticated user is get and pointed at request object.
#     """
#     @csrf_exempt
#     def wrap(request, *args, **kwargs):
#         encoded_jwt = request.META.get('Authorization', request.META.get('HTTP_AUTHORIZATION', '')).split(' ')[-1]
#         decoded_jwt = jwt.decode(encoded_jwt, key=settings.SECRET_KEY, leeway=30, algorithms=['HS256'])
#         user_id = decoded_jwt.get('user_id')
#         user = UserAuth.objects.get(uid=user_id)
#         request.user = user
#         request.user.__dict__['is_authenticated'] = True
#         return view(request, *args, **kwargs)
#     return wrap
