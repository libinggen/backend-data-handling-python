# urls.py
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "user"

urlpatterns = [
    path("", views.UserListView.as_view(), name="user-list"),
    path("user/<uuid:pk>", views.UserDetailView.as_view(), name="user-detail"),
    path("create-user", views.CreateUserView.as_view(), name="create-user"),
    path("update-user/<uuid:pk>", views.UpdateUserView.as_view(), name="update-user"),
    path("delete-user/<uuid:pk>", views.DeleteUserView.as_view(), name="delete-user"),
    path("error/", views.custom_error_view, name="custom-error"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
