# serializers.py
from rest_framework import serializers
from .models import User
from .utils import validate_password_complexity, handle_common_errors
import uuid


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate_uuid(self, value):
        # Check if the provided UUID is valid
        try:
            uuid_obj = uuid.UUID(value, version=4)
        except ValueError:
            raise serializers.ValidationError("Invalid UUID format.")

    def validate_name(self, value):
        # Check if the name starts with a letter
        if not value[0].isalpha():
            raise serializers.ValidationError("Name must start with a letter.")
        return value

    def validate_password(self, value):
        validate_password_complexity(value)
        return value

    def validate_new_password(self, value):
        validate_password_complexity(value)
        return value

    def validate(self, data):
        password_changed = False
        name_changed = False
        email_changed = False

        if "password" in data:
            password = data.get("password")
            if self.instance.password != data.get("password"):
                handle_common_errors("The password is incorrect.")

            if "new_password" in data:
                new_password = data.get("new_password")
                password_changed = password != new_password
                if not password_changed:
                    handle_common_errors(
                        "New password cannot be the same as the current password."
                    )
                data["password"] = new_password
                data["new_password"] = None

            if "name" in data:
                name = data.get("name")
                name_changed = name != self.instance.name
            if "email" in data:
                email = data.get("email")
                email_changed = email != self.instance.email

            if not (password_changed or name_changed or email_changed):
                handle_common_errors("The username is already in use.")

            if name_changed:
                existing_users = User.objects.filter(name=name)
                if existing_users.exists():
                    handle_common_errors("The username is already in use.")

            if email_changed:
                existing_users = User.objects.filter(email=email)
                if existing_users.exists():
                    handle_common_errors("The email is already in use.")

        else:
            handle_common_errors("Password is required.")

        return data
