from django.contrib.auth import get_user_model, user_logged_in, user_logged_out, \
    user_login_failed
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# logging, metrics, analytics, monitoring
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    logger.info(f"User {user} ({ip}) logged in")


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    logger.info(f"User {user} ({ip}) logged out")


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, **kwargs):
    logger.warning(f"Failed login attempt: {credentials}")