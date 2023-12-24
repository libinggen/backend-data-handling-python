# middleware.py
import logging
from django.db import IntegrityError
from django.db.utils import ProgrammingError
from django.http import JsonResponse
from rest_framework import status
from .utils import CustomError

logger = logging.getLogger(__name__)


class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, CustomError):
            # Log the custom error
            logger.error(f"Custom Error: {str(exception)}")

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
        ):
            # Log the exception
            logger.exception("Unhandled Exception")

            return JsonResponse(
                {"error": str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return None
