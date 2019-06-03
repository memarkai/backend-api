from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('consultation/create/', views.create_consultation),
    path('consultation/candidate/<uuid:consultation_id>/', views.candidate_for_consultation),
    path('consultation/candidate/list/<uuid:consultation_id>/', views.list_consultation_candidates),
    path('consultation/candidate/accept/<uuid:consultation_id>/', views.accept_candidate),
    path('consultation/candidate/refuse/<uuid:consultation_id>/', views.refuse_candidate),
    path('consultation/search/', views.search_consultation),
    path('consultation/search/clinic/open/', views.list_my_open_consultations),
]
