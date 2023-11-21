from parsing_helper.django_commands import create_admin

from eisz_downloader import models, settings


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

        models.Report.objects.all().delete()
        report_paths = []
        for report_path in self.settings.secrets.reports.paths:
            report_paths.append(models.Report(**report_path))
        models.Report.objects.bulk_create(report_paths)
        if len(report_paths) == 1:
            self.logger.info(f"{len(report_paths)} report path object was created.")
        else:
            self.logger.info(f"{len(report_paths)} report path objects were created.")
