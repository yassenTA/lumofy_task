from django.urls import path

from main.api.views import *

urlpatterns = [
    # User Routes
    path("login", LoginView.as_view(), name="login"),
    path("signup", RegisterView.as_view(), name="signup"),
    path("list_students", ListStudents.as_view(), name="list_students"),
    # Course CRUD routes
    path("create_course", CreateCourse.as_view(), name="create_course"),
    path("update_course", UpdateCourse.as_view(), name="update_course"),
    path("list_or_get_course", ListOrGetCourses.as_view(), name="list_or_get_course"),
    path("delete_course", DeleteCourse.as_view(), name="delete_course"),
    # Lessons Routes
    path("create_lesson", CreateLessonCourse.as_view(), name="create_lesson"),
    path(
        "add_or_remove_lesson",
        AddingOrRemovingLessonFromCourse.as_view(),
        name="add_or_remove_lesson",
    ),
    # Tracking Routes
    path("track_student", TrackingStudentProgress.as_view(), name="track_student"),
]
