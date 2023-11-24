from core.management.commands import core_browser_profile_command
from damumed import models
from damumed.management.commands import damumed_browser_command
from damumed.settings import Settings


class DamumedBrowserProfileCommand(
    core_browser_profile_command.CoreBrowserProfileCommand,
    damumed_browser_command.DamumedBrowserCommand
):
    settings = Settings()
    download_settings_model = models.DownloadSettings
    log_in_settings_model = models.LogInSettings
    parsing_settings_model = models.ParsingSettings

    get_cookies_path = damumed_browser_command.DamumedBrowserCommand.get_cookies_path
