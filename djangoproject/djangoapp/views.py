from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer, UserUpdateSerializer
from django.shortcuts import render


class UserListView(generics.ListCreateAPIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, pk):
        user = get_object_or_404(User, uuid=pk)
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateUserView(generics.RetrieveUpdateDestroyAPIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(generics.RetrieveUpdateDestroyAPIView):
    def put(self, request, pk):
        user = get_object_or_404(User, uuid=pk)
        serializer = UserUpdateSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(generics.RetrieveUpdateDestroyAPIView):
    def delete(self, request, pk):
        user = get_object_or_404(User, uuid=pk)
        user.delete()
        return Response("User successfully deleted!", status=status.HTTP_204_NO_CONTENT)


def custom_error_view(request, exception=None):
    return render(request, "custom_error.html", status=status.HTTP_404_NOT_FOUND)
