import datetime
import json
import os
import shutil
import time
from pathlib import Path

from pages import LogInPage, ReportsLogInPage, ReportsPage
from parser import models
from parser.management.commands import parser_browser_command


class DownloadNotFinishedException(Exception):
    pass


class Command(parser_browser_command.ParserBrowserCommand):
    begin_time: datetime.datetime
    end_time: datetime.datetime

    def before_command(self, log_in_settings: models.LogInSettings) -> None:
        super().before_command(log_in_settings)
        self.begin_time = datetime.datetime.now()

    def after_command(self, log_in_settings: models.LogInSettings) -> None:
        super().after_command(log_in_settings)
        log_in_settings.downloaded = True
        log_in_settings.save()

    def except_command(self, log_in_settings: models.LogInSettings) -> None:
        super().except_command(log_in_settings)
        log_in_settings.downloaded = False
        log_in_settings.save()

    def finally_command(self, log_in_settings: models.LogInSettings) -> None:
        self.end_time = datetime.datetime.now()
        log_in_settings.download_duration = self.end_time - self.begin_time
        log_in_settings.save()

    def wait_download(self) -> None:
        download_settings = models.DownloadSettings.get()
        for timer in range(download_settings.max_download_waiting):
            time.sleep(download_settings.download_check_period)
            for file in os.listdir(self.settings.TEMP_DOWNLOAD_FOLDER):
                if file.split('.')[-1] in self.settings.NOT_DOWNLOADED_EXTENSIONS:
                    break
            else:
                break
        else:
            raise DownloadNotFinishedException()

    def move(self, log_in_settings: models.LogInSettings, report: models.Report) -> None:
        files = {os.path.getctime(file): file for file in
                 (f"{self.settings.TEMP_DOWNLOAD_FOLDER}/{x}" for x in os.listdir(self.settings.TEMP_DOWNLOAD_FOLDER))}
        last_file: str = files[max(files)]

        folder = models.DownloadSettings.get().folder
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

    def run(self, log_in_settings: models.LogInSettings) -> None:
        self.remove_not_downloaded()
        log_in_page = LogInPage(self.driver)
        with open(self.get_cookies_path(log_in_settings)) as file:
            cookies = json.load(file)
            log_in_page.set_cookies(cookies)

        reports_log_in_page = ReportsLogInPage(self.driver)
        reports_log_in_page.log_in()

        for report in models.Report.objects.filter(download = True):
            counter = 3
            while True:
                try:
                    reports_page = ReportsPage(self.driver)
                    reports_page.open_report(report)
                    reports_page.set_period()
                    reports_page.set_filters()
                    reports_page.download_report()
                    self.wait_download()
                    self.move(log_in_settings, report)
                    break
                except Exception as error:
                    counter -= 1
                    if counter <= 0:
                        self.remove_not_downloaded()
                        raise error

        if os.path.exists(self.settings.TEMP_DOWNLOAD_FOLDER):
            shutil.rmtree(self.settings.TEMP_DOWNLOAD_FOLDER)
