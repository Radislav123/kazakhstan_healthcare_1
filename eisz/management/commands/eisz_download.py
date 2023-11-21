import json
import os
import shutil

from core.management.commands import core_download_command
from eisz import models
from eisz.management.commands import eisz_browser_command
from pages.eisz import LogInPage
from pages.eisz.reports import ReportsLogInPage, ReportsPage


class Command(eisz_browser_command.EISZBrowserCommand, core_download_command.CoreDownloadCommand):
    download_settings_model = models.DownloadSettings
    report_model = models.Report

    def run(self, log_in_settings: models.LogInSettings) -> None:
        self.remove_not_downloaded()
        log_in_page = LogInPage(self.driver)
        with open(self.get_cookies_path(log_in_settings)) as file:
            cookies = json.load(file)
            log_in_page.set_cookies(cookies)

        for report in self.report_model.objects.filter(download = True):
            counter = 3
            while True:
                try:
                    reports_log_in_page = ReportsLogInPage(self.driver)
                    reports_log_in_page.log_in()
                    reports_page = ReportsPage(self.driver)
                    reports_page.open_report(report)
                    reports_page.set_period()
                    reports_page.set_filters(report)
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
