import json

from core.management.commands import core_download_command
from damumed import models
from damumed.management.commands import damumed_browser_command, damumed_reports_download, damumed_screenings_download, \
    damumed_unloadings_download
from pages.damumed import MainPage, UnloadingPage


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
        run_screenings = damumed_screenings_download.Command.run
        run_unloading = damumed_unloadings_download.Command.run
        run_reports = damumed_reports_download.Command.run

        errors = []

        try:
            run_screenings(self, log_in_settings)
        except Exception as error:
            errors.append(error)
        try:
            run_unloading(self, log_in_settings)
        except Exception as error:
            errors.append(error)
        try:
            run_reports(self, log_in_settings)
        except Exception as error:
            errors.append(error)

        if errors:
            raise core_download_command.DownloadNotFinishedException() from errors[0]
