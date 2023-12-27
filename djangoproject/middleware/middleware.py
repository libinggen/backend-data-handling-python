# middleware/middleware.py
import logging
from django.http import JsonResponse
from django.db.utils import *
from django.core.exceptions import *
from rest_framework import status
from utils.exception_handler import CustomError

logger = logging.getLogger(__name__)


class CustomErrorMiddleware:
    """
    Initialize the CustomErrorMiddleware.

    Args:
        get_response (callable): The next middleware in the chain or the view.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        user_info = (
            f"User: {request.user.username} ({request.user.pk})"
            if request.user.is_authenticated
            else "Anonymous User"
        )
        return handle_custom_error(exception, user_info)


def handle_custom_error(exception, user_info):
    if isinstance(exception, CustomError):
        # Log the custom error
        logger.error(f"Custom Error: {str(exception)} {user_info}")
        return JsonResponse(
            {"error": str(exception)}, status=status.HTTP_400_BAD_REQUEST
        )
    elif (
        isinstance(exception, ProgrammingError)
        or isinstance(exception, TypeError)
        or isinstance(exception, UnboundLocalError)
        or isinstance(exception, AssertionError)
        or isinstance(exception, AttributeError)
        or isinstance(exception, IntegrityError)
        or isinstance(exception, KeyError)
        or isinstance(exception, FieldError)
        or isinstance(exception, ImproperlyConfigured)
    ):
        # Log the exception
        logger.exception(f"Unhandled Exception {user_info}")
        return JsonResponse(
            {"error": str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return None
