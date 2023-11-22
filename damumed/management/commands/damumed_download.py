import os
import shutil

from core.management.commands import core_download_command
from damumed import models
from damumed.management.commands import damumed_browser_command


class Command(damumed_browser_command.DamumedBrowserCommand, core_download_command.CoreDownloadCommand):
    download_settings_model = models.DownloadSettings
    report_model = models.Report

    def run(self, log_in_settings: models.LogInSettings) -> None:
        self.remove_not_downloaded()
        raise NotImplementedError()

        if os.path.exists(self.settings.TEMP_DOWNLOAD_FOLDER):
            shutil.rmtree(self.settings.TEMP_DOWNLOAD_FOLDER)
