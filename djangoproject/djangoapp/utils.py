# djangoapp/utils.py
from .models import CustomUser


def is_username_or_email_exists(username=None, email=None):
    existing_users = (
        CustomUser.objects.filter(username=username)
        if username
        else CustomUser.objects.none()
    )
    username_exists = existing_users.exists()

    existing_users = (
        CustomUser.objects.filter(email=email) if email else CustomUser.objects.none()
    )
    email_exists = existing_users.exists()

    return username_exists, email_exists
