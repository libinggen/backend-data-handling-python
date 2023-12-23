# middleware.py
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
        return None
