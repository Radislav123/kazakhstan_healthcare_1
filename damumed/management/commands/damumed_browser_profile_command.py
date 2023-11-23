from core.management.commands import core_browser_profile_command
from damumed import models
from damumed.management.commands import damumed_command


class DamumedBrowserProfileCommand(
    damumed_command.DamumedCommand,
    core_browser_profile_command.CoreBrowserProfileCommand
):
    download_settings_model = models.DownloadSettings
    log_in_settings_model = models.LogInSettings
    parsing_settings_model = models.ParsingSettings
