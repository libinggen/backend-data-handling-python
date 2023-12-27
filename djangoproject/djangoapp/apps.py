# djangoapp/apps.py
from django.apps import AppConfig
from django.core.exceptions import MiddlewareNotUsed  # noqa
from django.db.models.signals import post_save
from utils.exception_handler import handle_errors


class DjangoappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "djangoapp"

    def ready(self):
        from djangoapp.models import CustomUser
        import djangoapp.signals

        # Connect the signal
        post_save.connect(djangoapp.signals.user_created_signal, sender=CustomUser)

        # Raise MiddlewareNotUsed exception if not using the middleware
        # handle_errors(MiddlewareNotUsed("Middleware is not used."))
