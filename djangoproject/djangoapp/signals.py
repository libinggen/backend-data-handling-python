# djangoapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from djangoapp.models import CustomUser

import logging

logger = logging.getLogger(__name__)


def log_user_created_signal(logger, user):
    logger.error(
        f"Create {user.__class__.__name__} User: {user.username} ({user.uuid})"
    )


@receiver(post_save, sender=CustomUser)
def user_created_signal(sender, instance, created, **kwargs):
    try:
        if created:
            # Log the user creation event
            log_user_created_signal(logger, instance)

            # Perform additional tasks here (e.g., send a welcome email, create related objects)
    except Exception as e:
        # Handle exceptions during signal processing
        logger.error(f"Error processing user_created_signal: {str(e)}")
