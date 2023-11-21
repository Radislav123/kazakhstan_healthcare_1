from typing import Type

from parsing_helper.django_commands import create_admin

from eisz_downloader import models, settings
from secret_keeper import SecretKeeper


class Command(create_admin.CreateAdminCommand):
    settings = settings.Settings()

    def handle(self, *args, **options) -> None:
        super().handle(*args, **options)
        self.prepare_db()

    def prepare_singleton(self, secret_module: SecretKeeper.Module, model: Type[models.SingletonModel]) -> None:
        download_settings = model(**secret_module.get_dict())
        download_settings.save()
        self.logger.info(f"The {download_settings} was created.")

    def prepare_several_objects(self, secret_module: SecretKeeper.Module, model: Type[models.EISZDownloaderModel]) -> None:
        model.objects.all().delete()
        objects = []
        for value in secret_module.values:
            objects.append(model(**value))
        model.objects.bulk_create(objects)
        if len(objects) == 1:
            # noinspection PyProtectedMember
            self.logger.info(f"{len(objects)} {model._meta.verbose_name} object was created.")
        else:
            # noinspection PyProtectedMember
            self.logger.info(f"{len(objects)} {model._meta.verbose_name_plural} objects were created.")

    def prepare_db(self) -> None:
        self.prepare_singleton(self.settings.secrets.download_settings, models.DownloadSettings)
        self.prepare_several_objects(self.settings.secrets.log_in_settings, models.LogInSettings)
        self.prepare_singleton(self.settings.secrets.parsing_settings, models.ParsingSettings)
        self.prepare_several_objects(self.settings.secrets.reports, models.Report)
