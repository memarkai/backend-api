from django.urls import path
from patients import views

app_name = 'patients'

urlpatterns = [
    path('get/<uuid:patient_id>/', views.get_patient),
    path('update/', views.update_patient),
    path('list/', views.list_patients),
]
