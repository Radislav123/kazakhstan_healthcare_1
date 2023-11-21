from core import settings
from eisz.apps import EISZDownloaderConfig


class Settings(settings.Settings):
    APP_NAME = EISZDownloaderConfig.name

    def __init__(self):
        super().__init__()

        # Пути предопределенных настроек
        self.SETTINGS_FOLDER = f"{self.SETTINGS_FOLDER}/eisz"
        self.DOWNLOAD_SETTINGS_PATH = f"{self.SETTINGS_FOLDER}/download.json"
        self.LOG_IN_SETTINGS_PATH = f"{self.SETTINGS_FOLDER}/log_in.json"
        self.PARSING_SETTINGS_PATH = f"{self.SETTINGS_FOLDER}/parsing.json"
        self.REPORTS_PATH = f"{self.SETTINGS_FOLDER}/reports.json"

        self.JS_CODE_FOLDER = "js"
        self.JS_REPLACE_CERTIFICATE_PATH = f"{self.JS_CODE_FOLDER}/eisz/replaceCertificate.js"

        self.DOWNLOAD_DATE_FORMAT = "%d.%m.%Y"
