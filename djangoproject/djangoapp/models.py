# djangoapp/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator
import uuid


class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(
        max_length=250,
        unique=True,
        validators=[EmailValidator(message="Enter a valid email address.")],
    )

    password = models.CharField(max_length=128, null=True, blank=True)
    password2 = models.CharField(max_length=128, null=True, blank=True)

    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        related_query_name="custom_user",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_set",
        related_query_name="custom_user",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    def save(self, *args, **kwargs):
        """
        Custom save method for the CustomUser model.
        Override the default save behavior to include additional logic.
        """
        # Your custom save logic here
        super().save(*args, **kwargs)
