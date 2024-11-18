from rest_framework import serializers
from python_django_problem.models import *


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"

    def validate_file(self, file):
        max_size_mb = 10
        max_size_kb = max_size_mb * 1024
        if file.size > max_size_kb * 1024:
            raise serializers.ValidationError(f"File size exceeds {max_size_mb}MB limit.")

        return file