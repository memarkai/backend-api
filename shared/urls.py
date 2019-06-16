from django.urls import path
from shared import views

urlpatterns = [
    path('create/<str:usertype>/', views.create_user),
    path('login/', views.login),
    path('specialty/create/', views.create_specialty),
    path('specialty/list/', views.list_specialties),
    path('specialty/get/<uuid:specialty_id>/', views.get_specialty),
    path('insurance/create/', views.create_health_insurance),
    path('insurance/list/', views.list_health_insurances),
]
