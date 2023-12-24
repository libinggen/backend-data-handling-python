# middleware.py
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
        elif isinstance(exception, ProgrammingError):
            return JsonResponse({"error": str(exception)}, status=500)
        elif isinstance(exception, TypeError):
            return JsonResponse({"error": str(exception)}, status=500)
        return None
