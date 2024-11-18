from django.contrib.auth.models import AbstractUser
from django.db import models


class Completions(models.Model):
    enroll = models.ForeignKey('Enroll', on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.enroll.students.user.email + "-" + self.enroll.lessons.name + "-" + str(self.status)


class Courses(models.Model):
    course_name = models.CharField(max_length=100, blank=True, null=True)


class Enroll(models.Model):
    students = models.ForeignKey(
        "Students", on_delete=models.CASCADE, blank=True, null=True
    )
    lessons = models.ForeignKey(
        "Lessons", on_delete=models.CASCADE, blank=True, null=True
    )
    courses = models.ForeignKey(
        Courses, on_delete=models.CASCADE, blank=True, null=True
    )
    def __str__(self):
        return self.students.user.email + "-" + self.lessons.name + "-" + self.courses.course_name


class Lessons(models.Model):
    courses = models.ForeignKey(
        Courses, on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.CharField(blank=True, null=True)


class Students(models.Model):
    user = models.ForeignKey("Users", on_delete=models.CASCADE, blank=True, null=True)


class TeacherCourses(models.Model):
    teacher = models.ForeignKey(
        "Teachers", on_delete=models.CASCADE, blank=True, null=True
    )
    courses = models.ForeignKey(
        Courses, on_delete=models.CASCADE, blank=True, null=True
    )


class Teachers(models.Model):
    user = models.ForeignKey("Users", on_delete=models.CASCADE, blank=True, null=True)


class Users(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=100, unique=True, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
