from pathlib import Path

from parsing_helper import settings as helper_settings

from core.apps import CoreConfig


class Settings(helper_settings.Settings):
    APP_NAME = CoreConfig.name

    def __init__(self):
        super().__init__()

        self.PROJECT_FOLDER = str(Path(__file__).resolve().parent.parent.resolve())

        self.LOG_IN_FOLDER = f"{self.SECRETS_FOLDER}/log_in"
        self.AUTH_COOKIES_PATH = f"{self.LOG_IN_FOLDER}/cookies_placeholder.json"

        # Пути предопределенных настроек
        self.SETTINGS_FOLDER = f"{self.SECRETS_FOLDER}/settings"
        self.DOWNLOAD_SETTINGS_PATH = None
        self.LOG_IN_SETTINGS_PATH = None
        self.PARSING_SETTINGS_PATH = None
        self.REPORTS_PATH = None
        self.SCREENING_REPORTS_PATH = None
        self.CORE_SETTINGS_PATH = f"{self.SETTINGS_FOLDER}/core.json"

        self.JS_CODE_FOLDER = "js"

        self.TEMP_DOWNLOAD_FOLDER = str(Path(f"{self.PROJECT_FOLDER}/downloads_temp").resolve())
        self.CLEAR_TEMP_DOWNLOAD_FOLDER = True
        # noinspection SpellCheckingInspection
        self.NOT_DOWNLOADED_EXTENSIONS = ("tmp", "crdownload")

        self.CHROME_PROFILE_FOLDER = f"{self.PROJECT_FOLDER}/chrome_profile/User Data"
