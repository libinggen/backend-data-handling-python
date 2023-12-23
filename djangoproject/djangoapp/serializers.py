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

    # def validate_name(self, value):
    #     existing_users = User.objects.filter(name=value)

    #     if self.instance:
    #         existing_users = existing_users.exclude(pk=self.instance.pk)

    #     if existing_users.exists():
    #         handle_common_errors("The username is already in use.")

    #     return value

    # def validate_email(self, value):
    #     existing_users = User.objects.filter(email=value)

    #     if self.instance:
    #         existing_users = existing_users.exclude(pk=self.instance.pk)

    #     if existing_users.exists():
    #         handle_common_errors("The email is already in use.")

    #     return value

    def validate_password(self, value):
        try:
            validate_password_complexity(value)
        except ValueError as e:
            handle_common_errors(str(e))

        return value

    def validate(self, data):
        if "password" in data:

            def check_password_same(password_same):
                if not password_same:
                    handle_common_errors("The password is incorrect.")

            password_same = self.instance.password == data.get("password")

            if "name" in data:
                name = data.get("name")
                if name != self.instance.name:
                    existing_users = User.objects.filter(name=name)
                    if existing_users.exists():
                        handle_common_errors("The username is already in use.")
                    else:
                        check_password_same(password_same)
                        return data

            if "email" in data:
                email = data.get("email")
                if email != self.instance.email:
                    existing_users = User.objects.filter(email=email)
                    if existing_users.exists():
                        handle_common_errors("The email is already in use.")
                    else:
                        check_password_same(password_same)
                        return data

            if password_same:
                handle_common_errors(
                    "New password cannot be the same as the current password."
                )
        else:
            handle_common_errors("Password is required.")

        return data
