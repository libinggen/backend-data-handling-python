# utils/exception_handler.py
import re
from django.forms import ValidationError


class CustomError(Exception):
    def __init__(self, error_messages, status_code=None):
        self.error_messages = error_messages
        self.status_code = status_code


def handle_errors(error_messages, status_code=None):
    if isinstance(error_messages, str):
        error_messages = [error_messages]

    raise CustomError(error_messages, status_code=status_code)


def handle_validation_errors(error_messages, status_code=None):
    if isinstance(error_messages, str):
        error_messages = [error_messages]

    raise ValidationError(detail=error_messages, code=status_code)


def validate_password_complexity(password):
    # Maximum length check
    if len(password) > 14:
        handle_validation_errors("Password should be 14 characters or less.")

    # Minimum length check
    if len(password) < 8:
        handle_validation_errors("Password must be at least 8 characters long.")

    # Uppercase and lowercase letters check
    if not re.search(r"[a-z]", password) or not re.search(r"[A-Z]", password):
        handle_validation_errors(
            "Password must include both uppercase and lowercase letters."
        )

    # Numeric character check
    if not re.search(r"\d", password):
        handle_validation_errors(
            "Password must include at least one numeric character."
        )

    # Special character check
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        handle_validation_errors(
            "Password must include at least one special character."
        )

    # Common words check (you can customize this list)
    COMMON_WORDS = ["password", "123456", "qwerty", "admin"]
    for word in COMMON_WORDS:
        if word.lower() in password.lower():
            handle_validation_errors(
                f"Password should not contain common words like '{word}'."
            )
