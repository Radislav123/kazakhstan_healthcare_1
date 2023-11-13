from parsing_helper.django_commands import create_admin

from parser import models, settings


class Command(create_admin.CreateAdminCommand):
    settings = settings.Settings()

    def handle(self, *args, **options) -> None:
        super().handle(*args, **options)
        self.prepare_db()

    def prepare_db(self) -> None:
        download_settings = models.DownloadSettings(**self.settings.secrets.download_settings.get_dict())
        download_settings.save()
        self.logger.info(f"The {download_settings} was created.")

        log_in_settings = models.LogInSettings(**self.settings.secrets.log_in_settings.get_dict())
        log_in_settings.save()
        self.logger.info(f"The {log_in_settings} was created.")

        parsing_settings = models.ParsingSettings(**self.settings.secrets.parsing_settings.get_dict())
        parsing_settings.save()
        self.logger.info(f"The {parsing_settings} was created.")
