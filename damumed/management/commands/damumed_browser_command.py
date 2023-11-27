from selenium.webdriver import Chrome

from core.management.commands import core_browser_command
from damumed import models
from damumed.management.commands import damumed_command


class DamumedBrowserCommand(damumed_command.DamumedCommand, core_browser_command.CoreBrowserCommand):
    driver: Chrome
    download_settings_model = models.DownloadSettings
    log_in_settings_model = models.LogInSettings
    parsing_settings_model = models.ParsingSettings
    use_chrome_profile = True

    def get_cookies_path(self, log_in_settings: models.LogInSettings) -> str:
        return self.settings.AUTH_COOKIES_PATH.replace("placeholder", f"damumed_{log_in_settings.id}")
