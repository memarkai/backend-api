from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Text, Keyword, Date, GeoPoint, Search
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from . import models

connections.create_connection()

class ConsultationIndex(Document):
    clinic = Keyword()
    clinic_location = GeoPoint(lat_lon=True) 
    doctor = Keyword()
    specialty = Keyword()
    patient = Keyword()
    start_date = Date()
    end_date = Date()

    class Index:
        name = 'consultations-index'

def bulk_indexing():
    ConsultationIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=[
        c.indexing() for c in models.Consultation.objects.all().iterator()
    ])

def __executor__(search, page_from=None, page_size=20):
    page_from = page_from if page_from else 0
    page_size = page_size if page_size else 20
    return search[page_from:page_from + page_size].execute()

def consultations_between_two_dates(start: str, end: str, page_from=0):
    s = Search()\
        .filter('range', start_date={'gte': start})\
        .filter('rage', end_date={'lte': end})
    return __executor__(s, page_from)

def consultations_later_than_date(date: str, page_from=0):
    s = Search().filter('range', start_date={'gte': date})
    return __executor__(s, page_from)

def consultations_sooner_than_date(date: str, page_from=0):
    s = Search().filter('range', start_date={'lte': date})
    return __executor__(s, page_from)

def consultations_by_clinic(clinic_id: str, page_from=0):
    s = Search().filter('term', clinic=clinic_id)
    return __executor__(s, page_from)

def consultations_by_doctor(doctor_id: str, page_from=0):
    s = Search().filter('term', doctor=doctor_id)
    return __executor__(s, page_from)

def consultations_by_specialty(specialty_id: str, page_from=0):
    s = Search().filter('term', specialty=specialty_id)
    return __executor__(s, page_from)

def consultations_by_patient(patient_id: str, page_from=0):
    s = Search().filter('term', patient=patient_id)
    return __executor__(s, page_from)

def consultations_inside_radius(location, radius: float, page_from=0):
    s = Search()\
        .filter('geo_distance', distance=f'{radius}m', location=location)
    return __executor__(s, page_from)