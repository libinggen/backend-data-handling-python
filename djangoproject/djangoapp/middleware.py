# middleware.py
from django.db import IntegrityError
from django.db.utils import ProgrammingError
from django.http import JsonResponse
from .utils import CustomError


class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, CustomError):
            return JsonResponse({"error": str(exception)}, status=400)
        elif (
            isinstance(exception, ProgrammingError)
            or isinstance(exception, TypeError)
            or isinstance(exception, UnboundLocalError)
            or isinstance(exception, AssertionError)
            or isinstance(exception, AttributeError)
            or isinstance(exception, IntegrityError)
        ):
            return JsonResponse({"error": str(exception)}, status=500)
        return None
