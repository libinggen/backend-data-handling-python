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
        existing_users = User.objects.filter(name=value)

        if self.instance:
            existing_users = existing_users.exclude(pk=self.instance.pk)

        if existing_users.exists():
            handle_common_errors("The username is already in use.")

        return value

    def validate_email(self, value):
        existing_users = User.objects.filter(email=value)

        if self.instance:
            existing_users = existing_users.exclude(pk=self.instance.pk)

        if existing_users.exists():
            handle_common_errors("The email is already in use.")

        return value

    def validate_password(self, value):
        try:
            validate_password_complexity(value)
        except ValueError as e:
            handle_common_errors(str(e))

        # Check if the new password is the same as the current password
        if self.instance and self.instance.password == value:
            handle_common_errors(
                "New password cannot be the same as the current password."
            )

        return value
