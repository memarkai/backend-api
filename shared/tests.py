import json
from django.test import TestCase
from clinics.models import ClinicUser
from patients.models import PatientUser
from .models import HealthInsurance, HealthInsuranceSerializer, Specialty, SpecialtySerializer, BaseProfile
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

# Create your tests here.

class UnitTests(APITestCase):

    clinic = {
        "email": "clinic@testinho.com",
        "password": "clinicpass"
    }

    patient = {
        "email": "patient@testinho.com",
        "password": "patientpass"
    }

    def setUp(self):
        self.client = APIClient()
    
    def test_create_get_clinic_user(self):
        '''
            Tests the creation of a clinic using the routes implemented in shared views
        '''
        response = self.client.post("http://localhost:8000/api/create/clinic/", self.clinic, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        login_response = self.client.post("http://localhost:8000/api/login/", self.clinic, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        token = login_response.content.decode("utf-8")
        print("token received = " + token)
        
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

        get_myself_response = self.client.get("http://localhost:8000/api/clinics/get/")
        print(get_myself_response)
        self.assertEqual(get_myself_response.status_code, status.HTTP_200_OK)
        
        clinic_response = json.loads(get_myself_response.content)
        print(clinic_response)

        self.assertEqual(clinic_response["email"], self.clinic["email"])

    def test_create_patient_user(self):
        '''
            Tests the creation of a patient using the routes implemented in shared views
        '''
        response = self.client.post("http://localhost:8000/api/create/patient/", self.clinic, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        login_response = self.client.post("http://localhost:8000/api/login/", self.clinic, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = login_response.content.decode("utf-8")
       
        print("token received = " + token)

