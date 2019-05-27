from django.test import TestCase
from .models import Consultation
from clinics.models import ClinicUser, Doctor
from patients.models import PatientUser
from shared.models import Specialty
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
