import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


logger = logging.getLogger()


class Command(BaseCommand):
    """Creates default superuser in the database."""

    def add_arguments(self, parser):
        parser.add_argument('--debug', action='store_true')

    def handle(self, *args, **options):
        User = get_user_model()
        if (admin_user_set := User.objects.filter(username=settings.DJANGO_SUPERUSER_LOGIN)).exists():
            logger.info("Superuser already exists")
            admin_user = admin_user_set.last()
            admin_user.username = settings.DJANGO_SUPERUSER_LOGIN
            admin_user.set_password(settings.DJANGO_SUPERUSER_PASSWORD)
            admin_user.save()
            logger.info("Superuser credentials updated successfully")
            return
        User.objects.create_superuser(
            username=settings.DJANGO_SUPERUSER_LOGIN,
            password=settings.DJANGO_SUPERUSER_PASSWORD,
        )
        logger.info("Default superuser created successfully")
