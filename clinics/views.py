from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions
from shared.decorators import IsClinic, IsPatient, IsTokenAuthenticated
from .models import ClinicUser, ClinicUserSerializer, Doctor, DoctorSerializer
from shared.models import HealthInsurance, Specialty
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required
# Create your views here.

@api_view(['GET'])
@permission_classes((IsTokenAuthenticated & IsClinic, ))
def get_myself(request):
    clinic_json = ClinicUserSerializer(request.user.clinic) 
    return JsonResponse(clinic_json.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((IsTokenAuthenticated, ))
def get_clinic(request, clinic_id):
    clinic = get_object_or_404(ClinicUser, id=clinic_id)
    clinic_json = ClinicUserSerializer(clinic)
    return JsonResponse(clinic_json.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsTokenAuthenticated & IsClinic,))
def update_clinic(request):
    clinic = request.user.clinic
    clinic.update(
        phone=request.data.get('phone', clinic.phone),
        name=request.data.get('name', clinic.name),
        address=request.data.get('address', clinic.address),
        latitude=float(request.data.get('latitude', clinic.latitude)),
        longitude=float(request.data.get('longitude', clinic.longitude)),
    )
    return HttpResponse(status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((IsTokenAuthenticated & permissions.IsAdminUser, ))
def list_clinics(request):
    clinics_list = ClinicUser.objects.all()
    paginator = Paginator(clinics_list, 20)
    page = request.GET.get('page')
    clinics = paginator.get_page(page)
    page_json = ClinicUserSerializer(clinics, many=True)
    return JsonResponse(
        page_json.data,
        safe=False,
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes((IsTokenAuthenticated & IsClinic, ))
def create_doctor(request):
    specialty = get_object_or_404(Specialty, id=request.data['specialtyId'])
    Doctor.objects.create(
        crm=request.data['crm'],
        name=request.data['name'],
        specialty=specialty,
        clinic=request.user.clinic,
    )
    return HttpResponse(status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((IsTokenAuthenticated, IsClinic | IsPatient ))
def list_doctors(request, clinic_id=None):
    clinic = get_object_or_404(ClinicUser, id=clinic_id) if clinic_id else request.user.clinic
    doctors_list = clinic.list_doctors()
    paginator = Paginator(doctors_list, 20)
    page = request.GET.get('page')
    doctors = paginator.get_page(page)
    page_json = DoctorSerializer(doctors, many=True)
    return JsonResponse(
        page_json.data,
        safe=False,
        status=status.HTTP_200_OK
    )
