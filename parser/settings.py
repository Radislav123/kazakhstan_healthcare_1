from parsing_helper import settings as helper_settings

from .apps import ParserConfig


class Settings(helper_settings.Settings):
    APP_NAME = ParserConfig.name

    def __init__(self):
        super().__init__()

        # Пути предопределенных настроек
        self.SETTINGS_FOLDER = f"{self.SECRETS_FOLDER}/settings"
        self.DOWNLOAD_SETTINGS_PATH = f"{self.SETTINGS_FOLDER}/download.json"
        self.LOG_IN_SETTINGS_PATH = f"{self.SETTINGS_FOLDER}/log_in.json"
        self.PARSING_SETTINGS_PATH = f"{self.SETTINGS_FOLDER}/parsing.json"

        self.LOG_IN_FOLDER = f"{self.SECRETS_FOLDER}/log_in_driver"
        self.LOG_IN_DRIVER_DATA_PATH = f"{self.LOG_IN_FOLDER}/data.json"
        self.AUTH_COOKIES_PATH = f"{self.LOG_IN_FOLDER}/cookies.json"
