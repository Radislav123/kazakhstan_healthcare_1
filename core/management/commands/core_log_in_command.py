from core import models
from core.management.commands import core_browser_command


class CoreLogInCommand(core_browser_command.CoreBrowserCommand):
    def run(self, log_in_settings: models.LogInSettingsModel) -> None:
        raise NotImplementedError()

    def before_command(self, log_in_settings: models.LogInSettingsModel) -> None:
        log_in_settings.logged_in = None
        log_in_settings.downloaded = None
        log_in_settings.download_duration = None
        log_in_settings.save()
        super().before_command(log_in_settings)

    def after_command(self, log_in_settings: models.LogInSettingsModel) -> None:
        super().after_command(log_in_settings)
        log_in_settings.logged_in = True
        log_in_settings.save()

    def except_command(self, log_in_settings: models.LogInSettingsModel) -> None:
        super().except_command(log_in_settings)
        log_in_settings.logged_in = False
        log_in_settings.save()
