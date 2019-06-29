from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .models import PatientUser, PatientUserSerializer
from shared.decorators import IsPatient, IsTokenAuthenticated
from shared.models import HealthInsurance
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from rest_framework import status
# Create your views here.

@api_view(['POST'])
@permission_classes((IsTokenAuthenticated & IsPatient, ))
def update_patient(request):
    patient = request.user.patient
    insurance = patient.insurance
    if request.data.get('insurance'):
        insurance = request.data['insurance']
    PatientUser.objects.filter(id = patient.id).update(
        phone=request.data.get('phone', patient.phone),
        name=request.data.get('name', patient.name),
        address=request.data.get('address', patient.address),
        search_radius=request.data.get('search_radius', patient.search_radius),
        image=request.data.get('image', patient.image),
        insurance=insurance,
    )
    return HttpResponse(status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((IsTokenAuthenticated, ))
def get_patient(request, patient_id):
    patient = get_object_or_404(PatientUser, id=patient_id)
    patient_json = PatientUserSerializer(patient)
    return JsonResponse(patient_json.data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((IsTokenAuthenticated & permissions.IsAdminUser, ))
def list_patients(request):
    patients_list = PatientUser.objects.all()
    paginator = Paginator(patients_list, 20)
    page = request.GET.get('page')
    patients = paginator.get_page(page)
    page_json = PatientUserSerializer(patients, many=True)
    return JsonResponse(
        page_json.data,
        safe=False,
        status=status.HTTP_200_OK
    ) 
