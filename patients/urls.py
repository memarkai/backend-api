from django.urls import path

from patients import views


app_name = 'patients'
urlpatterns = [
    path('login', views.patient_login, name='login'),
]
