from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from main.api.serializer import (
    RegisterSerializer,
    LoginSerializer,
    CourseSerializer,
    LessonSerializer,
    StudentSerializer,
)
from main.models import Courses, Lessons, Students, Completions, Enroll


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})

        return context


class CreateCourse(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer

    def create(self, request, *args, **kwargs):
        if not request.data.get("course_name"):
            return Response(
                {"course_name": "This field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)


class UpdateCourse(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer

    def update(self, request, *args, **kwargs):
        if not request.data.get("course_id"):
            return Response(
                {"course_id": "This field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not request.data.get("course_name"):
            return Response(
                {"course_name": "This field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        course = Courses.objects.filter(id=request.data["course_id"]).first()
        if not course:
            return Response(
                {"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(instance=course, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class ListOrGetCourses(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer

    def list(self, request, *args, **kwargs):
        if request.query_params.get("course_id"):
            courses = Courses.objects.filter(
                id=request.query_params.get("course_id")
            ).first()
            serializer = self.serializer_class(courses)
        else:
            courses = Courses.objects.all()
            serializer = self.serializer_class(courses, many=True)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class DeleteCourse(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer

    def delete(self, request, *args, **kwargs):
        if not request.query_params.get("course_id"):
            return Response(
                {"course_id": "This field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        courses = Courses.objects.filter(
            id=request.query_params.get("course_id")
        ).first()
        if not courses:
            return Response(
                {"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND
            )
        courses.delete()
        return Response(
            {"message": "Course deleted successfully."}, status=status.HTTP_200_OK
        )


class CreateLessonCourse(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer

    def create(self, request, *args, **kwargs):
        if not request.data.get("name"):
            return Response(
                {"name": "This field is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)


class AddingOrRemovingLessonFromCourse(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer

    def update(self, request, *args, **kwargs):
        final_data = []
        if not request.data.get("course_id"):
            return Response(
                {"course_id": "This field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        course = Courses.objects.filter(id=request.data["course_id"]).first()
        if not course:
            return Response(
                {"error": "Course not found."}, status=status.HTTP_400_BAD_REQUEST
            )

        for data in request.data.get("lessons_status"):
            if not data.get("lesson_id"):
                return Response(
                    {"lesson_id": "This field is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            lesson = Lessons.objects.filter(id=data.get("lesson_id")).first()
            if not lesson:
                return Response(
                    {"error": "Lesson not found."}, status=status.HTTP_400_BAD_REQUEST
                )

            if data.get("add_or_remove") == 1:
                lesson.courses = course
                lesson.save()
            else:
                lesson.courses = None
                lesson.save()
            serializer = self.serializer_class(lesson)
            final_data.append(serializer.data)
        return Response({"data": final_data}, status=status.HTTP_200_OK)


class ListStudents(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer

    def list(self, request, *args, **kwargs):
        students = Students.objects.all()
        if not students:
            return Response(
                {"error": "No students found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(students, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class TrackingStudentProgress(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if not request.query_params.get("student_id"):
            return Response(
                {"student_id": "This field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        student = Students.objects.filter(
            id=request.query_params.get("student_id")
        ).first()
        if not student:
            return Response(
                {"error": "Student not found."}, status=status.HTTP_400_BAD_REQUEST
            )

        progress = []
        enrolls = Enroll.objects.filter(students=student).values_list(
            "lessons", flat=True
        )
        lessons = Lessons.objects.filter(id__in=enrolls)
        for lesson in lessons:
            data = {}
            completed = Completions.objects.filter(
                enroll__students=student, enroll__lessons=lesson
            ).first()
            data["lesson_name"] = completed.enroll.lessons.name
            data["is_completed"] = True if completed.status else False
            progress.append(data)
        student_progress = Completions.objects.filter(enroll__students=student)
        progress_count = student_progress.count()
        completed_lessons = student_progress.filter(status=True).count()
        percent = completed_lessons / progress_count
        data = {
            "student_name": student.user.name,
            "progress_per_lesson": progress,
            "percentage": str(percent * 100)+"%",
        }
        return Response({"data": data}, status=status.HTTP_200_OK)
