from django.urls import path
from .views import CVUploadView

urlpatterns = [
    path("cv/", CVUploadView.as_view(), name="cv-upload"),
]
