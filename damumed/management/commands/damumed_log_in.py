from core.management.commands import core_log_in_command
from damumed import models
from damumed.management.commands import damumed_browser_profile_command


class Command(damumed_browser_profile_command.DamumedBrowserProfileCommand, core_log_in_command.CoreLogInCommand):
    log_in_settings_model = models.LogInSettings

    def run(self, log_in_settings: models.LogInSettings) -> None:
        url = "https://vk.com/"
        print(f"opening {url}")
        self.driver.get(url)
        input(f"{url} was opened")
