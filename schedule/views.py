from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from shared.decorators import IsTokenAuthenticated, IsClinic, IsPatient
from clinics.models import Doctor, ClinicUser
from patients.models import PatientUser, PatientUserSerializer
from .models import Consultation, ConsultationSerializer
from schedule import search
from django.core.paginator import Paginator
from schedule import search
import datetime
# Create your views here.

@api_view(['POST'])
@permission_classes((IsTokenAuthenticated, IsClinic, ))
def create_consultation(request):
    doctor = get_object_or_404(Doctor, id=request.data['doctor'])
    Consultation.objects.create(
        clinic=request.user.clinic,
        doctor=doctor,
        start_date=datetime.datetime.strptime(
            request.data['startDate'], '%d/%m/%Y %H:%M:%S'
        ),
        end_date=datetime.datetime.strptime(
            request.data['endDate'], '%d/%m/%Y %H:%M:%S'
        )
    )
    return HttpResponse(status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsTokenAuthenticated, IsPatient, ))
def candidate_for_consultation(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    consultation.candidates.add(request.user.patient)
    consultation.save()
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsTokenAuthenticated, IsClinic))
def list_consultation_candidates(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    paginator = Paginator(consultation.candidates.all(), 20)
    page = request.GET.get('page')
    candidates = paginator.get_page(page)
    page_json = PatientUserSerializer(candidates, many=True)
    return JsonResponse(page_json.data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((IsTokenAuthenticated, IsClinic))
def list_my_consultations(request, scope):
    clinic_id = request.user.clinic.id
    page = request.GET.get('page')
    search_resp = search.list_consultations(clinic_id, scope, page_from=page)
    hits = search_resp['hits']['hits']
    return JsonResponse(hits, safe=False, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsTokenAuthenticated, IsClinic))
def accept_candidate(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id, clinic=request.user.clinic)
    consultation.accept_or_remove_candidate(request.data['patient'])
    return HttpResponse(status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsTokenAuthenticated, IsClinic))
def refuse_candidate(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id, clinic=request.user.clinic)
    consultation.accept_or_remove_candidate(request.data['patient'], accept=False)
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsTokenAuthenticated, ))
def search_consultation(request):
    page = request.query_params.get('page', 0)
    search_resp = search.search_consultation(request.data, page)
    hits = search_resp['hits']['hits']
    return JsonResponse(hits, safe=False, status=status.HTTP_200_OK)
