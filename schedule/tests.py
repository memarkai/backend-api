from django.test import TestCase
from .models import Consultation
from clinics.models import ClinicUser, Doctor
from patients.models import PatientUser
from shared.models import Specialty
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import datetime
import uuid

# Create your tests here.
class ConsultationTestCase(TestCase):

    def setUp(self):
        clinic = ClinicUser.objects.create(
            email=f'{str(uuid.uuid4()).replace("-", "")}@tests.com',
            password=str(uuid.uuid4())
        )
        specialty = Specialty.objects.create(
            name='lhebs'
        )
        doctor = Doctor.objects.create(
            name=str(uuid.uuid4()), 
            crm='123456/PE', 
            specialty=specialty,
            clinic=clinic
        )
        consultation = Consultation.objects.create(
            clinic=clinic,
            doctor=doctor,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(minutes=20)
        )

    def test0_consultation_creation(self):
        clinic = ClinicUser.objects.create(
            email=f'{str(uuid.uuid4()).replace("-", "")}@tests.com',
            password=str(uuid.uuid4())
        )
        specialty = Specialty.objects.create(
            name='lhebs'
        )
        doctor = Doctor.objects.create(
            name=str(uuid.uuid4()), 
            crm='123456/PE', 
            specialty=specialty,
            clinic=clinic
        )
        consultation = Consultation.objects.create(
            clinic=clinic,
            doctor=doctor,
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now() + datetime.timedelta(minutes=20)
        )

    def test1_consultation_candidation(self):
        patient = PatientUser.objects.create(
            email=f'{str(uuid.uuid4()).replace("-", "")}@tests.com',
            password=str(uuid.uuid4())
        )
        consultation = Consultation.objects.all()[0]
        consultation.candidates.add(patient)
        consultation.save()
        self.assertGreater(len(consultation.candidates.all()), 0)


class ConsultationAPITestCase(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.host = 'http://localhost:8000'
        self.clinic = ClinicUser.objects.create(
            email=f'{str(uuid.uuid4()).replace("-", "")}@tests.com',
            password=str(uuid.uuid4())
        )
        self.specialty = Specialty.objects.create(
            name='lhebs'
        )
        self.doctor = Doctor.objects.create(
            name=str(uuid.uuid4()), 
            crm='123456/PE', 
            specialty=specialty,
            clinic=clinic
        )
        self.consultation_mock = {
            'startDate': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'endDate':(datetime.datetime.now() + datetime.timedelta(minutes=20)).strftime('%d/%m/%Y %H:%M:%S'),
            'doctor': str(self.doctor.id),
        }

    def test_create_consultation(self):
        response = self.client.post(f'{self.host}/api/schedule/consultation/create')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    