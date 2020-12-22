from django.contrib import admin
from django.urls import path
from Prediction import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="Home"),
    path('Donate/', views.donate, name="Donate"),
    path('Hospitals/', views.Hospitals, name="BestHospitals"),
    path('Graph/', views.graph, name="Graph"),
    path('Check/', views.Check, name="PredictionPage"),
    path('Prediction/', views.Prediction, name="PredictionOut"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)