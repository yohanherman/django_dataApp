
from django.urls import path
from . import views 

urlpatterns = [
    path('', views. import_csv , name='index'), 
    path('consommation-par-region/', views.consumption_by_region, name='consommation_par_region'),
    path('consommation-par-annee/', views.consumption_by_year, name='consommation_par_annee'),
  
]
