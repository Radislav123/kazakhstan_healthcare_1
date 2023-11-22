from core.management.commands import core_log_in_command
from damumed import models
from damumed.management.commands import damumed_browser_command


class Command(damumed_browser_command.DamumedBrowserCommand, core_log_in_command.CoreLogInCommand):
    log_in_settings_model = models.LogInSettings

    def run(self, log_in_settings: models.LogInSettings) -> None:
        raise NotImplementedError
