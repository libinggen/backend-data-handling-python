# serializers/serializers.py
import uuid
from rest_framework import serializers
from utils.exception_handler import (
    handle_validation_errors,
    validate_password_complexity,
)


class UUIDSerializer(serializers.Serializer):
    def validate_uuid(self, value):
        try:
            uuid_obj = uuid.UUID(value, version=4)
        except ValueError:
            handle_validation_errors("Invalid UUID format.")


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=8,
        max_length=14,
        allow_null=False,
        allow_blank=False,
        required=True,
    )
    password2 = serializers.CharField(min_length=8, max_length=14, required=False)

    def validate_password(self, value):
        validate_password_complexity(value)
        return value

    def validate_password2(self, value):
        validate_password_complexity(value)
        return value
