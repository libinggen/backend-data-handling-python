# serializers.py
from rest_framework import serializers
from .models import User
from .utils import validate_password_complexity, handle_common_errors
import uuid


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uuid", "name", "email", "password"]

    name = serializers.CharField(min_length=3, max_length=50)
    email = serializers.EmailField(min_length=5, max_length=250)
    password = serializers.CharField(min_length=8, max_length=14)

    def validate_uuid(self, value):
        # Check if the provided UUID is valid
        try:
            uuid_obj = uuid.UUID(value, version=4)
        except ValueError:
            raise handle_common_errors("Invalid UUID format.")

    def validate_name(self, value):
        if not value[0].isalpha():
            raise handle_common_errors("Name must start with a letter.")
        return value

    def validate_password(self, value):
        validate_password_complexity(value)
        return value

    def validate_new_password(self, value):
        validate_password_complexity(value)
        return value


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uuid", "name", "email", "password", "new_password"]

    name = serializers.CharField(required=False, min_length=3, max_length=50)
    email = serializers.EmailField(required=False, min_length=5, max_length=250)
    password = serializers.CharField(
        required=True, min_length=8, max_length=14, allow_null=False, allow_blank=False
    )
    new_password = serializers.CharField(required=False, min_length=8, max_length=14)

    def validate_name(self, value):
        # Check if the name starts with a letter
        if not value[0].isalpha():
            handle_common_errors("Name must start with a letter.")
        return value

    def validate_password(self, value):
        validate_password_complexity(value)
        return value

    def validate_new_password(self, value):
        validate_password_complexity(value)
        return value

    def validate(self, data):
        error_messages = []
        password_changed = False
        name_exists = False
        email_exists = False

        if "password" in data:
            password = data.get("password")
            if self.instance.password != data.get("password"):
                handle_common_errors("The password is incorrect.")

            if not ("new_password" in data or "name" in data or "email" in data):
                handle_common_errors("Must include new password or name or email.")
            if "new_password" in data:
                new_password = data.get("new_password")
                password_changed = password != new_password
                if not password_changed:
                    handle_common_errors(
                        "New password cannot be the same as the current password."
                    )
                data["password"] = new_password
                data["new_password"] = None

            if not password_changed:
                if "name" in data:
                    name = data.get("name")
                    existing_users = User.objects.filter(name=name)
                    name_exists = existing_users.exists()
                    if name_exists and not "email" in data:
                        handle_common_errors("The username is already in use.")

                if "email" in data:
                    email = data.get("email")
                    existing_users = User.objects.filter(email=email)
                    email_exists = existing_users.exists()
                    if email_exists and not "name" in data:
                        handle_common_errors("The email is already in use.")

                if name_exists and email_exists:
                    error_messages.append("The username is already in use.")
                    error_messages.append("The email is already in use.")
                    handle_common_errors(error_messages)
        else:
            handle_common_errors("Password is required.")

        return data
