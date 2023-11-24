import json
from pathlib import Path

from core.management.commands import core_log_in_command
from damumed import models
from damumed.management.commands import damumed_browser_profile_command
from pages.damumed import LogInPage, MainPage


class Command(damumed_browser_profile_command.DamumedBrowserProfileCommand, core_log_in_command.CoreLogInCommand):
    log_in_settings_model = models.LogInSettings

    def run(self, log_in_settings: models.LogInSettings) -> None:
        main_page = MainPage(self.driver)
        main_page.log_out()

        log_in_page = LogInPage(self.driver)
        log_in_page.log_in(log_in_settings)
        main_page.log_out_button.reset()
        main_page.log_out_button.init()

        Path(self.settings.LOG_IN_FOLDER).mkdir(parents = True, exist_ok = True)
        with open(self.get_cookies_path(log_in_settings), 'w') as file:
            json.dump(self.driver.get_cookies(), file, indent = 4)
