import json
from pathlib import Path

from pages import DigitalLogInPage, LogInPage
from parser import models
from parser.management.commands import parser_browser_command


class Command(parser_browser_command.ParserBrowserCommand):
    def run(self, log_in_settings: models.LogInSettings) -> None:
        log_in_page = LogInPage(self.driver)
        log_in_page.log_in(log_in_settings.iin, log_in_settings.password)

        digital_log_in_page = DigitalLogInPage(self.driver)
        digital_log_in_page.log_in(log_in_settings)

        Path(self.settings.LOG_IN_FOLDER).mkdir(parents = True, exist_ok = True)
        with open(self.get_cookies_path(log_in_settings), 'w') as file:
            json.dump(self.driver.get_cookies(), file, indent = 4)
