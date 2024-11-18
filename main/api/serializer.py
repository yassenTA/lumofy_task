from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from main.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "name", "gender", "email"]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=Users.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = (
            "email",
            "password",
            "password2",
            "name",
            "gender",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"error": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        email = validated_data["email"]
        user = Users.objects.create(
            email=email, name=validated_data["name"], gender=validated_data["gender"]
        )
        user.set_password(validated_data["password"])
        user.save()

        return user


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["user_id"] = str(user.id)
        return token

    def handel_error(self, error):
        print(error)
        if isinstance(error.detail, list) and len(error.detail) == 1:
            error.detail = error.detail[0]
        elif isinstance(error.detail, str):
            pass
            # error_response.data = get_response(
            #     message=error[0], status_code=error_response.status_code)
        elif isinstance(error, dict):
            pass
        raise error

    def validate(self, attrs):
        email = attrs.get("email")

        data = {}

        user = Users.objects.get(email=email)
        user.save()
        attrs["email"] = user.email
        data = super(LoginSerializer, self).validate(attrs)
        user_serializer = UserSerializer(user)
        data.update({"user_data": user_serializer.data})
        return data


class CourseSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(required=True)

    class Meta:
        model = Courses
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(required=False)
    class Meta:
        model = Lessons
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Students
        fields = "__all__"
