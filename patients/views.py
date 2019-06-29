from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .models import PatientUser, PatientUserSerializer
from shared.decorators import IsPatient, IsTokenAuthenticated
from shared.models import HealthInsurance, BaseProfile
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from rest_framework import status
# Create your views here.

@api_view(['POST'])
@permission_classes((IsTokenAuthenticated & IsPatient, ))
def update_patient(request):
    user = request.user
    insurance = user.patient.insurance
    if request.data.get('insurance'):
        insurance = HealthInsurance.objects.get(id=request.data['insurance'])
    if request.data.get('image'):
        image = request.FILES['image']
        fs = FileSystemStorage(location='images/')
        filename = fs.save(image.name, image)
        file_path = fs.url
    else:
        file_path=None
    print(file_path)
    BaseProfile.objects.filter(id = user.id).update(
        phone=request.data.get('phone', user.phone),
        name=request.data.get('name', user.name),
        address=request.data.get('address', user.address),
        image=file_path
    )
    PatientUser.objects.filter(id = user.patient.id).update(
        search_radius=request.data.get('search_radius', user.patient.search_radius),        
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
