import os.path
import shutil

from core import models as core_models
from core.management.commands import core_command


class Command(core_command.CoreCommand):
    def handle(self, *args, **options) -> None:
        self.remove_profile()
        self.copy_profile()

    def remove_profile(self) -> None:
        if os.path.exists(self.settings.CHROME_PROFILE_COPY_FOLDER):
            shutil.rmtree(self.settings.CHROME_PROFILE_COPY_FOLDER)

    def copy_profile(self) -> None:
        shutil.copytree(core_models.CoreSettings.get().chrome_profile_folder, self.settings.CHROME_PROFILE_COPY_FOLDER)
