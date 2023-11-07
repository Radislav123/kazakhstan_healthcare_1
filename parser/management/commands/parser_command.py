from parsing_helper.django_commands import django_command

from parser import settings


class TelegramParserCommand(django_command.BaseCommand):
    settings = settings.Settings()

    def __init__(self) -> None:
        super().__init__()
