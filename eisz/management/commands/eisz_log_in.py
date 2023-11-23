import json
from pathlib import Path

from core.management.commands import core_log_in_command
from eisz import models
from eisz.management.commands import eisz_browser_command
from pages.eisz import LogInPage, SignatureLogInPage


class Command(eisz_browser_command.EISZBrowserCommand, core_log_in_command.CoreLogInCommand):
    log_in_settings_model = models.LogInSettings

    def run(self, log_in_settings: models.LogInSettings) -> None:
        log_in_page = LogInPage(self.driver)
        log_in_page.log_in(log_in_settings.iin, log_in_settings.password)

        digital_log_in_page = SignatureLogInPage(self.driver)
        digital_log_in_page.log_in(log_in_settings)

        Path(self.settings.LOG_IN_FOLDER).mkdir(parents = True, exist_ok = True)
        with open(self.get_cookies_path(log_in_settings), 'w') as file:
            json.dump(self.driver.get_cookies(), file, indent = 4)
