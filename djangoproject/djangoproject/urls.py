# djangoproject/urls.py

"""
Utility functions for the Django application.
Includes helper functions for handling user data and other common tasks.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="Notes API")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("rest_framework.urls")),
    path("jwtauth/", include("jwtauth.urls"), name="jwtauth"),
    path("users/", include("djangoapp.urls")),
    path("docs/", schema_view),
]
