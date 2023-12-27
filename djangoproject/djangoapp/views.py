# djangoapp/views.py
import logging
from django.urls import reverse
from django.http import Http404
from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
)

logger = logging.getLogger(__name__)


def log_exception(logger, view_name, exception, user):
    logger.exception(
        f"Error in {view_name}: {exception} User: {user.username} ({user.pk})"
    )


class BaseUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def handle_exception(self, exc):
        user = self.request.user
        log_exception(logger, self.__class__.__name__, exc, user)
        if isinstance(exc, (ValueError, ValidationError)):
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(exc, Http404):
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)

    def get_detail_url(self, uuid):
        return reverse("user:user-detail", kwargs={"uuid": uuid})


class UserListView(BaseUserView, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = CustomUser.objects.all().filter(is_staff=False)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)

            detail_url = self.get_detail_url(serializer.data[0]["uuid"])
            return Response(
                {
                    "data": serializer.data,
                    "detail_url": detail_url,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return self.handle_exception(e)


class UserDetailView(BaseUserView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = CustomUser.objects.all().filter(is_staff=False)
    serializer_class = UserSerializer
    lookup_field = "uuid"

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, uuid=kwargs["uuid"])
            serializer = self.get_serializer(instance)

            detail_url = self.get_detail_url(kwargs["uuid"])
            return Response(
                {
                    "data": serializer.data,
                    "detail_url": detail_url,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return self.handle_exception(e)


class UpdateUserView(BaseUserView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = CustomUser.objects.all().filter(is_staff=False)
    serializer_class = UserUpdateSerializer
    lookup_field = "uuid"

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop("partial", False)
            # Fetch the user instance to be updated
            instance = get_object_or_404(self.queryset, uuid=kwargs["uuid"])
            # Create a serializer instance for the user update
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            # Validate the serializer data
            serializer.is_valid(raise_exception=True)
            # Update the user's password if provided in the request
            if "password" in request.data:
                serializer.validated_data["password"] = make_password(
                    request.data["password"]
                )
            # Perform the update
            self.perform_update(serializer)

            # Retrieve user data for the response
            user_instance = serializer.instance
            user_data = {
                "uuid": user_instance.uuid,
                "username": user_instance.username,
                "email": user_instance.email,
            }

            res = {
                "user": user_data,
            }

            # Generate the detail URL for the response
            detail_url = self.get_detail_url(kwargs["uuid"])
            return Response(
                {
                    "data": res,
                    "detail_url": detail_url,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            # Handle exceptions and return an appropriate response
            return self.handle_exception(e)


class DeleteUserView(BaseUserView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = CustomUser.objects.all().filter(is_staff=False)
    serializer_class = UserSerializer
    lookup_field = "uuid"

    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(self.queryset, uuid=kwargs["uuid"])
            self.perform_destroy(instance)

            detail_url = self.get_detail_url(kwargs["uuid"])
            return Response(
                {
                    "detail": "User successfully deleted!",
                    "detail_url": detail_url,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return self.handle_exception(e)


def custom_error_view(request, exception=None):
    return render(request, "custom_error.html", status=status.HTTP_404_NOT_FOUND)
