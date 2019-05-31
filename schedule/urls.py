from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    path('consultation/create/', views.create_consultation),
    path('consultation/candidate/', views.candidate_for_consultation),
    path('consultation/candidate/accept/', views.accept_candidate),
    path('consultation/search/', views.search_consultation),
]
