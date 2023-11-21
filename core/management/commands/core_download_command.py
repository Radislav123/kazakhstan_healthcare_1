import datetime
import os
import time
from pathlib import Path
from typing import Type

from core import models
from core.management.commands import core_browser_command


class DownloadNotFinishedException(Exception):
    pass


class CoreDownloadCommand(core_browser_command.CoreBrowserCommand):
    download_settings_model: Type[models.DownloadSettingsModel]
    report_model: Type[models.ReportModel]
    begin_time: datetime.datetime
    end_time: datetime.datetime

    def before_command(self, log_in_settings: models.LogInSettingsModel) -> None:
        super().before_command(log_in_settings)
        self.begin_time = datetime.datetime.now()

    def after_command(self, log_in_settings: models.LogInSettingsModel) -> None:
        super().after_command(log_in_settings)
        log_in_settings.downloaded = True
        log_in_settings.save()

    def except_command(self, log_in_settings: models.LogInSettingsModel) -> None:
        super().except_command(log_in_settings)
        log_in_settings.downloaded = False
        log_in_settings.save()

    def finally_command(self, log_in_settings: models.LogInSettingsModel) -> None:
        self.end_time = datetime.datetime.now()
        log_in_settings.download_duration = self.end_time - self.begin_time
        log_in_settings.save()
        super().finally_command(log_in_settings)

    def wait_download(self) -> None:
        download_settings = self.download_settings_model.get()
        for timer in range(download_settings.max_download_waiting):
            time.sleep(download_settings.download_check_period)
            for file in os.listdir(self.settings.TEMP_DOWNLOAD_FOLDER):
                if file.split('.')[-1] in self.settings.NOT_DOWNLOADED_EXTENSIONS:
                    break
            else:
                break
        else:
            raise DownloadNotFinishedException()

    def move(self, log_in_settings: models.LogInSettingsModel, report: models.ReportModel) -> None:
        files = {os.path.getctime(file): file for file in
                 (f"{self.settings.TEMP_DOWNLOAD_FOLDER}/{x}" for x in os.listdir(self.settings.TEMP_DOWNLOAD_FOLDER))}
        last_file: str = files[max(files)]

        folder = self.download_settings_model.get().folder
        if log_in_settings.folder:
            folder += f"/{log_in_settings.folder}"
        if report.folder:
            folder += f"/{report.folder}"

        Path(folder).mkdir(parents = True, exist_ok = True)
        os.replace(last_file, f"{folder}/{report.name}.{last_file.split('.')[-1]}")

    def remove_not_downloaded(self) -> None:
        if os.path.exists(self.settings.TEMP_DOWNLOAD_FOLDER):
            files = (file for file in (f"{self.settings.TEMP_DOWNLOAD_FOLDER}/{x}"
                                       for x in os.listdir(self.settings.TEMP_DOWNLOAD_FOLDER)))
            for file in files:
                if file.split('.')[-1] in self.settings.NOT_DOWNLOADED_EXTENSIONS:
                    os.remove(file)

    def run(self, log_in_settings: models.LogInSettingsModel) -> None:
        raise NotImplementedError()
