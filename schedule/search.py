from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Text, Keyword, Date, GeoPoint, Search, Q
from elasticsearch import Elasticsearch
from rest_framework.exceptions import ValidationError
from elasticsearch.helpers import bulk
from django.utils.translation import ugettext_lazy as _
from . import models

connections.create_connection()
es = Elasticsearch()

class ConsultationIndex(Document):
    clinic = Keyword()
    clinic_location = GeoPoint(lat_lon=True) 
    doctor = Keyword()
    specialty = Keyword()
    patient = Keyword()
    candidates = Text()
    startDate = Date()
    endDate = Date()

    class Index:
        name = 'consultations-index'

def bulk_indexing():
    ConsultationIndex.init()
    bulk(client=es, actions=[
        c.indexing() for c in models.Consultation.objects.all().iterator()
    ])

def __executor__(search, page_from=None, page_size=2000):
    page_from = page_from if page_from else 0
    return search[page_from:page_from + page_size].execute().to_dict()

def list_consultations(clinic_id, scope, page_from=0):
    s = ConsultationIndex.search()
    if scope == 'all':
        s = s.query('bool', must=[Q('match', clinic=clinic_id)])
    elif scope == 'open':
        s = s.query('bool', must=[Q('match', clinic=clinic_id)], filter=[~Q('exists', field='patient')])
    elif scope == 'closed':
        s = s.query('bool', must=[Q('match', clinic=clinic_id)], filter=[Q('exists', field='patient')])
    else:
        raise ValidationError(_('Invalid scope'))
    return __executor__(s, page_from)


def list_all_candidates_for_clinic(clinic_id):
    s = ConsultationIndex.search()
    s = s.query('bool', must=[Q('match', clinic=clinic_id)], filter=[Q('exists', field='candidates')])
    return __executor__(s, 0)


def list_doctor_schedule(doctor_id, start_date, end_date):
    s = ConsultationIndex.search()
    s = s.query('bool', must=[Q('range', startDate={'gte': start_date}), Q('range', endDate={'lte': end_date}), Q('match', doctor=doctor_id)])
    return __executor__(s, 0, 200)

def search_consultation(query_dict, page_from=0):
    query_type = list(query_dict.keys())[0]
    s = ConsultationIndex.search().query(query_type, **query_dict[query_type])
    return __executor__(s, page_from)

def delete_consultation(consultation_id):
    s = ConsultationIndex.search().query('match', _id=consultation_id)
    return s.delete()