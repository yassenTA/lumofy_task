from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status

from main.models import Users


# Old Function
def register_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = Users.objects.get(username=username, password=password, email=email)
        return JsonResponse({"message": "User Created"})


# New Function

def register_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        if not username:
            return JsonResponse({"username": "username is required"}, status=status.HTTP_400_BAD_REQUEST)

        password = request.POST.get('password')
        if not password:
            return JsonResponse({"password": "password is required"}, status=status.HTTP_400_BAD_REQUEST)

        email = request.POST.get('email')
        if not email:
            return JsonResponse({"email": "email is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists by username or email
        exist = Users.objects.filter(Q(username=username)|Q(email=email)).first()
        if exist:
            return JsonResponse({"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        #Password not assigned to model directly without hashing
        user = Users.objects.create_user(username=username, email=email)
        user.set_password(password)

        # .save() method is missing
        user.save()

        # Return a success response with HTTP status code 201 (Created)
        return JsonResponse({"message": "User Created"}, status=status.HTTP_201_CREATED)
