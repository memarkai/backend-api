from django.urls import path

from clinics import views


app_name = 'clinics'
urlpatterns = [
    path('login', views.clinic_login, name='login'),
]
