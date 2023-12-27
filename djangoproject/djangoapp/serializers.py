# djangoapp/serializers.py
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from serializers.serializers import PasswordSerializer, UUIDSerializer
from utils.exception_handler import handle_validation_errors
from .utils import is_username_or_email_exists
from .models import CustomUser


class UserSerializer(UUIDSerializer, PasswordSerializer, serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["uuid", "username", "email"]


class UserUpdateSerializer(
    UUIDSerializer, PasswordSerializer, serializers.ModelSerializer
):
    """
    Serializer for updating user data.

    Includes validation for username, email, and password updates.
    """

    class Meta:
        model = CustomUser
        fields = ["uuid", "username", "email", "password", "password2"]

    username = serializers.CharField(min_length=3, max_length=50, required=False)
    email = serializers.EmailField(min_length=5, max_length=250, required=False)

    def validate_username(self, value):
        if not value[0].isalpha():
            handle_validation_errors("Username must start with a letter.")
        return value

    def validate(self, data):
        """
        Validate the serializer data.

        Args:
            data (dict): The data to be validated.

        Returns:
            dict: The validated data.

        Raises:
            CustomError: If validation fails.
        """

        error_messages = []
        password_changed = False
        username_exists = False
        email_exists = False
        username = None
        email = None

        if "password" in data:
            password = data.get("password")
            if not check_password(password, self.instance.password):
                handle_validation_errors("The password is incorrect.")

            if not ("password2" in data or "username" in data or "email" in data):
                handle_validation_errors(
                    "Must include new password or username or email."
                )
            if "password2" in data:
                password2 = data.get("password2")
                password_changed = password != password2
                if not password_changed:
                    handle_validation_errors(
                        "New password cannot be the same as the current password."
                    )
                data["password"] = password2
                data["password2"] = None

            if not password_changed:
                if "username" in data:
                    username = data.get("username")
                if "email" in data:
                    email = data.get("email")

                if username:
                    username_exists, _ = is_username_or_email_exists(username=username)
                    if username_exists and (not email or email == self.instance.email):
                        handle_validation_errors("The username is already in use.")

                if email:
                    _, email_exists = is_username_or_email_exists(email=email)
                    if email_exists and (
                        not username or username == self.instance.username
                    ):
                        error_messages.append("The email is already in use.")

                if error_messages:
                    handle_validation_errors(error_messages)
        else:
            handle_validation_errors("Password is required.")

        return data
