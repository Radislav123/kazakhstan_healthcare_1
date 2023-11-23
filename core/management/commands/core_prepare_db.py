from typing import Type

from core import models, settings
from core.management.commands import core_command
from secret_keeper import SecretKeeper


class Command(core_command.CoreCommand):
    settings = settings.Settings()

    def handle(self, *args, **options) -> None:
        self.prepare_db()

    def prepare_singleton(self, secret_module: SecretKeeper.Module, model: Type[models.CoreSingletonModel]) -> None:
        download_settings = model(**secret_module.get_dict())
        download_settings.save()
        self.logger.info(f"The {download_settings} was created.")

    def prepare_db(self) -> None:
        self.prepare_singleton(self.settings.secrets.core_settings, models.CoreSettings)
