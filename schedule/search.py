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
    start_date = Date()
    end_date = Date()

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
    return search.execute()

def search_consultation(query_dict, page_from=0):
    s = Q(**query_dict)
    return __executor__(s, page_from)