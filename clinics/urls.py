from django.urls import path
from clinics import views

app_name = 'clinics'

urlpatterns = [
    path('get/', views.get_myself),
    path('get/<uuid:clinic_id>/', views.get_clinic),
    path('update/', views.update_clinic),
    path('list/', views.list_clinics),
    path('doctor/create/', views.create_doctor),
    path('doctor/list/', views.list_doctors),
    path('doctor/list/<uuid:clinic_id>/', views.list_doctors),
]
