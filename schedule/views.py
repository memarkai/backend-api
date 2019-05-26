from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from shared.decorators import IsTokenAuthenticated, IsClinic, IsPatient
from clinics.models import Doctor, ClinicUser
from patients.models import PatientUser
from .models import Consultation, ConsultationSerializer
from schedule import search
from django.core.paginator import Paginator
import datetime
# Create your views here.

@api_view(['POST'])
@permission_classes((IsTokenAuthenticated & IsClinic, ))
def create_consultation(request):
    doctor = get_object_or_404(Doctor, id=request.data['doctor'])
    Consultation.objects.create(
        clinic=request.user,
        doctor=doctor,
        start_date=datetime.datetime.strptime(
            request.data['startDate'], '%d/%m/%Y %H:%M:S'
        ),
        end_date=datetime.datetime.strptime(
            request.data['endDate'], '%d/%m/%Y %H:%M:%S'
        )
    )
    return HttpResponse(status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsTokenAuthenticated & IsPatient, ))
def candidate_for_consultation(request):
    consultation = get_object_or_404(Consultation, id=request.data['consultation'])
    consultation.candidates.add(request.user)
    consultation.save()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsTokenAuthenticated & IsClinic))
def accept_candidate(request):
    consultation = get_object_or_404(Consultation, id=request.data['consultation'], clinic=request.user)
    candidate = consultation.candidates.get(id=request.data['patient'])
    consultation.patient = candidate
    consultation.candidates.remove(candidate)
    consultation.save()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsTokenAuthenticated & IsClinic, ))
def list_clinic_consultations(request):
    consultations_list = request.user.consultation_set.all()
    paginator = Paginator(consultations_list, 20)
    page = request.get.GET('page')
    consultations = paginator.get_page(page)
    page_json = ConsultationSerializer(consultations, many=True)
    return JsonResponse(
        page_json,
        safe=False,
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes((IsTokenAuthenticated, ))
def list_consultations_between_dates(request):
    start_date = request.get.GET('start_date')
    end_date = request.get.GET('end_date')
    page = request.get.GET('page')
    hits = search.consultations_between_two_dates(start_date, end_date, page)
    return JsonResponse(hits, status=status.HTTP_200_OK)


