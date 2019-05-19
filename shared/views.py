from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework import permissions
from clinics.models import ClinicUser
from patients.models import PatientUser
from .models import HealthInsurance, HealthInsuranceSerializer, Specialty, SpecialtySerializer, BaseProfile
from .decorators import IsTokenAuthenticated
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
# Create your views here.

@api_view(['POST'])
def create_user(request, usertype):
    klass = PatientUser if usertype == 'patient' else ClinicUser
    user = klass.objects.create(
        email=request.data['email'],
        password=request.data['password'],
    )
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
def login(request):
    # klass = PatientUser if usertype == 'patient' else ClinicUser
    jwt_token = BaseProfile.authenticate(
        request.data['email'], request.data['password']
    )
    return HttpResponse(jwt_token.decode(), status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsTokenAuthenticated & permissions.IsAdminUser, ))
def create_specialty(request):
    Specialty.objects.create(name=request.data['name'])
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsTokenAuthenticated & permissions.IsAdminUser, ))
def create_health_insurance(request):
    HealthInsurance.objects.create(name=request.data['name'])
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsTokenAuthenticated, ))
def list_specialties(request):
    specialties_list = Specialty.objects.all()
    paginator = Paginator(specialties_list, 20)
    page = request.GET.get('page')
    specialties = paginator.get_page(page)
    page_json = SpecialtySerializer(specialties, many=True)
    return JsonResponse(
        page_json.data,
        safe=False,
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes((IsTokenAuthenticated, ))
def list_health_insurances(request):
    health_insurances_list = HealthInsurance.objects.all()
    paginator = Paginator(health_insurances_list, 20)
    page = request.GET.get('page')
    health_insurances = paginator.get_page(page)
    page_json = HealthInsuranceSerializer(health_insurances, many=True)
    return JsonResponse(
        page_json.data,
        safe=False,
        status=status.HTTP_200_OK
    )