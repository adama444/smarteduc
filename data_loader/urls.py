from django.urls import path
from . import views

app_name = "data_loader"

urlpatterns = [
    path("upload/", views.upload_file, name="upload"),
]
