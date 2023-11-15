import json
from pathlib import Path

from pages import DigitalLogInPage, LogInPage
from parser.management.commands import parser_browser_command


class Command(parser_browser_command.ParserBrowserCommand):
    def run(self) -> None:
        log_in_page = LogInPage(self.driver)
        log_in_page.log_in(self.settings.secrets.log_in_settings.iin, self.settings.secrets.log_in_settings.password)

        digital_log_in_page = DigitalLogInPage(self.driver)
        digital_log_in_page.log_in()

        Path(self.settings.LOG_IN_FOLDER).mkdir(parents = True, exist_ok = True)
        with open(self.settings.AUTH_COOKIES_PATH, 'w') as file:
            json.dump(self.driver.get_cookies(), file, indent = 4)
