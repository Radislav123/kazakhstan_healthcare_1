from parsing_helper.django_commands import django_command

from eisz_downloader import settings


class EISZDownloaderCommand(django_command.BaseCommand):
    settings = settings.Settings()
