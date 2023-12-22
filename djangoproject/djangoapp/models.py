from django.db import models
import uuid


class User(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=250, unique=True)
    password = models.CharField(max_length=14, null=True, blank=True)
