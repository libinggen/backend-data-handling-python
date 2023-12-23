# serializers.py
from rest_framework import serializers
from .models import User
import re
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
            raise serializers.ValidationError("The username is already in use.")

        return value

    def validate_email(self, value):
        existing_users = User.objects.filter(email=value)

        if self.instance:
            existing_users = existing_users.exclude(pk=self.instance.pk)

        if existing_users.exists():
            raise serializers.ValidationError("The email is already in use.")

        return value

    def validate_password(self, value):
        # Maximum length check
        if len(value) > 14:
            raise serializers.ValidationError(
                "Password should be 14 characters or less."
            )

        # Minimum length check
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )

        # Uppercase and lowercase letters check
        if not re.search(r"[a-z]", value) or not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "Password must include both uppercase and lowercase letters."
            )

        # Numeric character check
        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "Password must include at least one numeric character."
            )

        # Special character check
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError(
                "Password must include at least one special character."
            )

        # Common words check (you can customize this list)
        common_words = ["password", "123456", "qwerty", "admin"]
        for word in common_words:
            if word.lower() in value.lower():
                raise serializers.ValidationError(
                    f"Password should not contain common words like '{word}'."
                )

        # Check if the new password is the same as the current password
        if self.instance and self.instance.password == value:
            raise serializers.ValidationError(
                "New password cannot be the same as the current password."
            )

        return value
