from rest_framework.decorators import api_view
from accounts.decorators import token_required
from accounts.models import UserAuth
from django.http import JsonResponse
# Create your views here.


@token_required
@api_view(['POST'])
def login(request):
    jwt_token = UserAuth.authenticate(
        request.data['email'],
        request.data['password']
    )
    return JsonResponse(jwt_token, status=200)
