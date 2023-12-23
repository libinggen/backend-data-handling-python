# urls.py
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "user"

urlpatterns = [
    path("", views.UserListView.as_view(), name="user-list"),
    path("create-user", views.UserListView.as_view(), name="create-user"),
    path("user/<uuid:pk>", views.UserDetailView.as_view(), name="user-detail"),
    path("update-user/<uuid:pk>", views.UserDetailView.as_view(), name="update-user"),
    path("delete-user/<uuid:pk>", views.UserDetailView.as_view(), name="delete-user"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
