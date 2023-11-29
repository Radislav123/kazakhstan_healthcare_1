from core import settings
from eisz.apps import EISZConfig


class Settings(settings.Settings):
    APP_NAME = EISZConfig.name

    def __init__(self):
        super().__init__()

        # Пути предопределенных настроек
        self.SETTINGS_FOLDER = f"{self.SETTINGS_FOLDER}/eisz"
        self.DOWNLOAD_SETTINGS_PATH = f"{self.SETTINGS_FOLDER}/download.json"
        self.LOG_IN_SETTINGS_PATH = f"{self.SETTINGS_FOLDER}/log_in.json"
        self.PARSING_SETTINGS_PATH = f"{self.SETTINGS_FOLDER}/parsing.json"
        self.REPORTS_PATH = f"{self.SETTINGS_FOLDER}/reports.json"

        self.JS_CODE_FOLDER = f"{self.JS_CODE_FOLDER}/eisz"
        self.JS_REPLACE_CERTIFICATE_PATH = f"{self.JS_CODE_FOLDER}/replaceCertificate.js"
