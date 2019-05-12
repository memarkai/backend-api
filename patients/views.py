from django.http import JsonResponse

from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from patients.models import PatientUser


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def patient_login(request):
    data = {
    	'jwt_token': PatientUser.authenticate(
	        request.data['email'],
	        request.data['password']
    	),
    }
    return JsonResponse(data, status=status.HTTP_200_OK)
