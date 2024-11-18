from django.db import models


# Create your models here.

class File(models.Model):
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to="file", blank=True, null=True)

    def __str__(self):
        return self.file_name
