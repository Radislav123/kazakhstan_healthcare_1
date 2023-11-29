import json

from core.management.commands import core_download_command
from damumed import models
from damumed.management.commands import damumed_browser_command
from pages.damumed import MainPage, UnloadingPage


class Command(damumed_browser_command.DamumedBrowserCommand, core_download_command.CoreDownloadCommand):
    download_settings_model = models.DownloadSettings

    def run(self, log_in_settings: models.LogInSettings) -> None:
        main_page = MainPage(self.driver)
        main_page.open()
        main_page.driver.delete_all_cookies()
        main_page.open()
        with open(self.get_cookies_path(log_in_settings)) as file:
            cookies = json.load(file)
            main_page.set_cookies(cookies)

        for report in models.UnloadingReport.objects.filter(download = True):
            counter = 3
            while True:
                try:
                    reports_page = UnloadingPage(self.driver)
                    reports_page.open()
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
