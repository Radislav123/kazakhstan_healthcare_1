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
        self.REPORT_PATHS_PATH = f"{self.SETTINGS_FOLDER}/report_paths.json"

        self.LOG_IN_FOLDER = f"{self.SECRETS_FOLDER}/log_in"
        self.AUTH_COOKIES_PATH = f"{self.LOG_IN_FOLDER}/cookies.json"

        self.JS_CODE_FOLDER = "js"
        self.JS_REPLACE_CERTIFICATE_PATH = f"{self.JS_CODE_FOLDER}/replaceCertificate.js"
