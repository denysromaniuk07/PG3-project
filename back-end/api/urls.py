from django.urls import path
from .views import hello


urlpatterns = [
    path("upload/", hello, name="upload"),
]
