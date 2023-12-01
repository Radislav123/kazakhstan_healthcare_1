import json

from core.management.commands import core_download_command
from damumed import models
from damumed.management.commands import damumed_browser_command
from pages.damumed import MainPage, ReportsPage


class Command(damumed_browser_command.DamumedBrowserCommand, core_download_command.CoreDownloadCommand):
    download_settings_model = models.DownloadSettings

    def before_command(self, log_in_settings: models.LogInSettings) -> None:
        super().before_command(log_in_settings)
        main_page = MainPage(self.driver)
        main_page.open()
        main_page.driver.delete_all_cookies()
        main_page.open()
        with open(self.get_cookies_path(log_in_settings)) as file:
            cookies = json.load(file)
            main_page.set_cookies(cookies)

    def run(self, log_in_settings: models.LogInSettings) -> None:
        errors = []
        for report in models.Report.objects.filter(download = True):
            try:
                counter = 3
                while True:
                    try:
                        reports_page = ReportsPage(self.driver)
                        reports_page.open_report(report)
                        reports_page.set_period()
                        reports_page.set_filters(report)
                        reports_page.set_checkbox_filters(report)
                        reports_page.set_multiple_filters(report)
                        reports_page.download_report()

                        self.wait_download()
                        self.move(log_in_settings, report)
                        # закрывает дополнительную вкладку
                        self.driver.close()
                        break
                    except Exception as error:
                        counter -= 1
                        if counter <= 0:
                            self.remove_not_downloaded()
                            raise error
            except Exception as error:
                errors.append(error)
        if errors:
            raise core_download_command.DownloadNotFinishedException() from errors[0]
