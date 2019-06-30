from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
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
@permission_classes((IsTokenAuthenticated, IsClinic, ))
def delete_consultation(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    consultation.delete()
    return HttpResponse(status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsTokenAuthenticated, IsPatient, ))
def candidate_for_consultation(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)        
    consultation.candidates.add(request.user.patient)
    consultation.save()
    return HttpResponse(status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((IsTokenAuthenticated, IsPatient, ))
def revoke_candidature_for_consultation(request, consultation_id):
    consultation = get_object_or_404(Consultation, id=consultation_id)
    if request.user.patient in consultation.candidates.all():
        consultation.candidates.remove(request.user.patient)
    elif consultation.patient == request.user.patient:
        consultation.patient = None
    else:
        raise NotFound('Patient is not a candidate for this consultation')
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


@api_view(['GET'])
@permission_classes((IsTokenAuthenticated, ))
def list_doctor_schedule(request, doctor_id):
    start_date = request.GET['startDate']
    end_date = request.GET['endDate']
    start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
    end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')
    search_resp = search.list_doctor_schedule(doctor_id, start_date, end_date)
    hits = search_resp['hits']['hits']
    response = [dict(consultation=h['_id'], status='closed' if h.get('patient') else 'open', **h['_source']) for h in hits]
    return JsonResponse(response, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsTokenAuthenticated, ))
def list_clinic_candidates(request, clinic_id):
    all_consultations = search.list_all_candidates_for_clinic(clinic_id)
    hits = all_consultations['hits']['hits']
    candidates_ids = []
    for h in hits:
        print(h)
        candidates_ids.extend([cid for cid in h['_source']['candidates']])
    return JsonResponse(candidates_ids, safe=False, status=status.HTTP_200_OK)