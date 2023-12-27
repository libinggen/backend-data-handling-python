# jwtauth/views.py
from rest_framework import permissions
from rest_framework import response, decorators, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserCreateSerializer, UserLoginSerializer


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    user = serializer.validated_data
    refresh = RefreshToken.for_user(user)

    user_data = {
        "uuid": user.uuid,
        "username": user.username,
        "email": user.email,
    }

    res = {
        "user": user_data,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

    return response.Response(res, status.HTTP_201_CREATED)


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def registration(request):
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)

    user_data = {
        "uuid": user.uuid,
        "username": user.username,
        "email": user.email,
    }

    res = {
        "user": user_data,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return response.Response(res, status.HTTP_201_CREATED)
