from core import settings
from damumed.apps import DamumedConfig


class Settings(settings.Settings):
    APP_NAME = DamumedConfig.name

    def __init__(self):
        super().__init__()

        # Пути предопределенных настроек
        self.SETTINGS_FOLDER = f"{self.SETTINGS_FOLDER}/damumed"
        self.DOWNLOAD_SETTINGS_PATH = f"{self.SETTINGS_FOLDER}/download.json"
        self.LOG_IN_SETTINGS_PATH = f"{self.SETTINGS_FOLDER}/log_in.json"
        self.PARSING_SETTINGS_PATH = f"{self.SETTINGS_FOLDER}/parsing.json"
        self.REPORTS_PATH = f"{self.SETTINGS_FOLDER}/reports.json"
        self.SCREENING_REPORTS_PATH = f"{self.SETTINGS_FOLDER}/screening_reports.json"
