from django.urls import get_script_prefix
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from python_django_problem.api.serializer import FileSerializer
from python_django_problem.models import File


class UploadFile(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FileSerializer

    def create(self, request, *args, **kwargs):
        if not request.FILES.get("file"):
            return Response({"error": "file is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get("file_name"):
            return Response({"error": "file_name is required"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data":serializer.data}, status=status.HTTP_201_CREATED)


class ListAllFiles(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FileSerializer
    def list(self, request, *args, **kwargs):
        files = File.objects.all()
        serializer = self.serializer_class(files, many=True).data
        data = []
        for instance in serializer:
            instance['file'] = request.build_absolute_uri(get_script_prefix()) + instance['file']
            data.append(instance)

        return Response({"data": data}, status=status.HTTP_200_OK)


class GetFile(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FileSerializer
    def list(self, request, *args, **kwargs):
        if not request.query_params.get("file_id"):
            return Response({"error": "file_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        file = File.objects.filter(id=request.query_params.get("file_id")).first()
        if not file:
            return Response({"error": "file not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(file).data
        serializer['file'] = request.build_absolute_uri(get_script_prefix()) + serializer['file']
        return Response({"data": serializer}, status=status.HTTP_200_OK)