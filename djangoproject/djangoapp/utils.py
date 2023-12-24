# utils.py
import re
from .models import User


class CustomError(Exception):
    def __init__(self, error_message):
        self.error_message = error_message


def handle_common_errors(error_message):
    raise CustomError(error_message)


def validate_password_complexity(password):
    # Maximum length check
    if len(password) > 14:
        raise CustomError("Password should be 14 characters or less.")

    # Minimum length check
    if len(password) < 8:
        raise CustomError("Password must be at least 8 characters long.")

    # Uppercase and lowercase letters check
    if not re.search(r"[a-z]", password) or not re.search(r"[A-Z]", password):
        raise CustomError("Password must include both uppercase and lowercase letters.")

    # Numeric character check
    if not re.search(r"\d", password):
        raise CustomError("Password must include at least one numeric character.")

    # Special character check
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise CustomError("Password must include at least one special character.")

    # Common words check (you can customize this list)
    COMMON_WORDS = ["password", "123456", "qwerty", "admin"]
    for word in COMMON_WORDS:
        if word.lower() in password.lower():
            raise CustomError(
                f"Password should not contain common words like '{word}'."
            )


def is_name_or_email_exists(name=None, email=None):
    existing_users = User.objects.filter(name=name) if name else User.objects.none()
    name_exists = existing_users.exists()

    existing_users = User.objects.filter(email=email) if email else User.objects.none()
    email_exists = existing_users.exists()

    return name_exists, email_exists
