from django.urls import path
from .views import GeneratePdf, GenerateAndDownloadPDF
urlpatterns = [
    path('', GeneratePdf.as_view()),
    path('pdf/', GenerateAndDownloadPDF.as_view()),
]
