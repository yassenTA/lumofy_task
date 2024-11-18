from django.urls import path

from python_django_problem.api.views import *

urlpatterns = [
        path("upload_file", UploadFile.as_view(), name="upload_file"),
        path("list_all_files", ListAllFiles.as_view(), name="list_all_files"),
        path("get_file", GetFile.as_view(), name="get_file"),
]
