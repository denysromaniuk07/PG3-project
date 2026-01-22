from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        # Try to authenticate with username first
        user = authenticate(username=username, password=password)
        
        # If authentication fails, try to find user by email and authenticate
        if not user:
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        })

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email", "")

        if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        """
        try:
            validate_password(password)
        except ValidationError as e:
            return Response(
                {"error": e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )
        """
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        refresh = RefreshToken.for_user(user)
        
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        })