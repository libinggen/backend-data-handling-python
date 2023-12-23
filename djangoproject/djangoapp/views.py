from django.db import IntegrityError
from django.forms import ValidationError
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer


@api_view(["GET"])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getUser(request, pk):
    try:
        user = User.objects.get(uuid=pk)
    except User.DoesNotExist:
        raise Http404("User does not exist")

    serializer = UserSerializer(instance=user, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)


@api_view(["POST"])
def addUser(request):
    serializer = UserSerializer(data=request.data)

    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    except IntegrityError as e:
        error_message = "User with this name or email already exists."
        return Response({"error": error_message}, status=400)
    except ValidationError as e:
        return Response({"error": str(e)}, status=400)


@api_view(["PUT"])
def updateUser(request, pk):
    try:
        user = User.objects.get(uuid=pk)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    serializer = UserSerializer(instance=user, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["DELETE"])
def deleteUser(request, pk):
    try:
        user = User.objects.get(uuid=pk)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    user.delete()
    return Response("User successfully deleted!")
