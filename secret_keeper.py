from typing import TYPE_CHECKING

from parsing_helper import secret_keeper


if TYPE_CHECKING:
    from parser.settings import Settings


class SecretKeeper(secret_keeper.SecretKeeper):
    Module = secret_keeper.SecretKeeper.Module

    class DownloadSettings(Module):
        download_folder: str

    class LogInSettings(Module):
        iin: int
        password: str

    class ParsingSettings(Module):
        show_folder: bool

    class ReportPaths(Module):
        paths: list[dict[str, str]]

    download_settings: DownloadSettings
    log_in_settings: LogInSettings
    parsing_settings: ParsingSettings
    report_paths: ReportPaths

    def __init__(self, settings: "Settings") -> None:
        super().__init__(settings)

        self.add_module("download_settings", settings.DOWNLOAD_SETTINGS_PATH)
        self.add_module("log_in_settings", settings.LOG_IN_SETTINGS_PATH)
        self.add_module("parsing_settings", settings.PARSING_SETTINGS_PATH)
        self.add_module("report_paths", settings.REPORT_PATHS_PATH)
