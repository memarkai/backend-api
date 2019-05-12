from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view

from clinics.models import ClinicUser


@api_view(['POST'])
def clinic_login(request):
    data = {
    	'jwt_token': ClinicUser.authenticate(
        	request.data['email'],
        	request.data['password']
    	),
    }
    return JsonResponse(data, status=status.HTTP_200_OK)
