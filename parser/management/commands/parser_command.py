from parsing_helper.django_commands import django_command

from parser import settings


class ParserCommand(django_command.BaseCommand):
    settings = settings.Settings()
