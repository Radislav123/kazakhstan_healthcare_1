from typing import TYPE_CHECKING

from parsing_helper import secret_keeper


if TYPE_CHECKING:
    from core.settings import Settings as CoreSettings


class SecretKeeper(secret_keeper.SecretKeeper):
    Module = secret_keeper.SecretKeeper.Module

    class CoreSettings(Module):
        chrome_profile_folder: str

    class DownloadSettings(Module):
        folder: str
        format: str
        max_download_waiting: int
        download_check_period: int

    class LogInSettings(Module):
        values: list[dict[str, str]]

    class ParsingSettings(Module):
        show_browser: bool

    class Reports(Module):
        values: list[dict[str, str]]

    core_settings: CoreSettings
    download_settings: DownloadSettings
    log_in_settings: LogInSettings
    parsing_settings: ParsingSettings
    reports: Reports

    def __init__(self, settings: "CoreSettings") -> None:
        super().__init__(settings)

        self.add_module("core_settings", settings.CORE_SETTINGS_PATH)
        if settings.DOWNLOAD_SETTINGS_PATH:
            self.add_module("download_settings", settings.DOWNLOAD_SETTINGS_PATH)
        if settings.LOG_IN_SETTINGS_PATH:
            self.add_module("log_in_settings", settings.LOG_IN_SETTINGS_PATH)
        if settings.PARSING_SETTINGS_PATH:
            self.add_module("parsing_settings", settings.PARSING_SETTINGS_PATH)
        if settings.REPORTS_PATH:
            self.add_module("reports", settings.REPORTS_PATH)
