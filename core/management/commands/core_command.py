from parsing_helper.django_commands import django_command

from core import settings


class CoreCommand(django_command.BaseCommand):
    settings = settings.Settings()
