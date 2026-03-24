from django.urls import path
from .views import download_report

urlpatterns = [
    path('', download_report, name='report'),
]
