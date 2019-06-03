from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Document, Text, Keyword, Date, GeoPoint, Search, Q
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
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

def __executor__(search, page_from=None, page_size=20):
    page_from = page_from if page_from else 0
    page_size = page_size if page_size else 20
    return search[page_from:page_from + page_size].execute().to_dict()


def open_consultations(clinic_id, page_from=0):
    s = ConsultationIndex.search().query('bool', must=[Q('match', clinic=clinic_id)], filter=[Q('missing', field='patient')])
    return __executor__(s, page_from)

def search_consultation(query_dict, page_from=0):
    query_type = list(query_dict.keys())[0]
    s = ConsultationIndex.search().query(query_type, **query_dict[query_type])
    return __executor__(s, page_from)