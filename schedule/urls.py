from django.urls import path, re_path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('consultation/create/', views.create_consultation),
    path('consultation/candidate/<uuid:consultation_id>/', views.candidate_for_consultation),
    path('consultation/candidate/list/<uuid:consultation_id>/', views.list_consultation_candidates),
    path('consultation/candidate/accept/<uuid:consultation_id>/', views.accept_candidate),
    path('consultation/candidate/refuse/<uuid:consultation_id>/', views.refuse_candidate),
    path('consultation/search/', views.search_consultation),
    re_path('consultation/search/(?P<scope>all|open|closed)?/', views.list_my_consultations),
]
