# jwtauth/serializers.py


from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers

from djangoapp.models import CustomUser
from serializers.serializers import PasswordSerializer
from utils.exception_handler import handle_validation_errors


class UserLoginSerializer(PasswordSerializer, serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=50, required=False)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, data):
        username = data["username"]
        password = data["password"]
        existing_users = (
            CustomUser.objects.filter(username=username)
            if username
            else CustomUser.objects.none()
        )
        username_exists = existing_users.exists()
        if not username_exists:
            handle_validation_errors("The user does not exist.")

        user = CustomUser.objects.get(username=username)
        if not check_password(password, user.password):
            handle_validation_errors("The password is incorrect.")
        return user


class UserCreateSerializer(PasswordSerializer, serializers.ModelSerializer):
    email = serializers.EmailField(max_length=250)
    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
        label="Confirm password",
    )

    class Meta:
        model = CustomUser
        fields = ["uuid", "username", "email", "password", "password2"]

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if (
            username
            and CustomUser.objects.filter(username=username)
            .exclude(email=email)
            .exists()
        ):
            handle_validation_errors({"name": "Username is already in use."})

        if (
            email
            and CustomUser.objects.filter(email=email)
            .exclude(username=username)
            .exists()
        ):
            handle_validation_errors({"email": "Email is already in use."})

        if password != password2:
            handle_validation_errors({"password": "The two passwords differ."})
        password_hash = make_password(password=password)
        user = CustomUser(username=username, email=email, password=password_hash)
        user.save()
        return user
