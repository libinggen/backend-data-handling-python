# views.py
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, UserUpdateSerializer


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     def get(self, request, pk):
#         user = get_object_or_404(User, uuid=pk)
#         serializer = UserSerializer(instance=user)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "uuid"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
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
