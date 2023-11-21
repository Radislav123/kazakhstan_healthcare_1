from selenium.webdriver import Chrome

from core.management.commands import core_browser_command
from eisz import models
from eisz.management.commands import eisz_command


class EISZBrowserCommand(eisz_command.EISZCommand, core_browser_command.CoreBrowserCommand):
    driver: Chrome
    log_in_settings_model = models.LogInSettings
    parsing_settings_model = models.ParsingSettings

    def get_cookies_path(self, log_in_settings: models.LogInSettings) -> str:
        return self.settings.AUTH_COOKIES_PATH.replace("placeholder", f"eisz_{log_in_settings.id}")
