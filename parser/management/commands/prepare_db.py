from parsing_helper.django_commands import create_admin

from parser import models


class Command(create_admin.CreateAdminCommand):
    def handle(self, *args, **options) -> None:
        super().handle(*args, **options)
        self.prepare_db()

    @staticmethod
    def prepare_db() -> None:
        download_settings = models.DownloadSettings(
            download_folder = r"C:\intellij_projects\freelance\kazakhstan_healthcare_1\downloads"
        )
        download_settings.save()

        parsing_settings = models.ParsingSettings(
            show_browser = True
        )
        parsing_settings.save()
