import pathlib
from typing import Type

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager

from core import models
from core.management.commands import core_command


class DownloadException(Exception):
    pass


class CoreBrowserCommand(core_command.CoreCommand):
    driver: Chrome
    download_settings_model: Type[models.DownloadSettingsModel]
    log_in_settings_model: Type[models.LogInSettingsModel]
    parsing_settings_model: Type[models.ParsingSettingsModel]
    use_chrome_profile: bool

    def handle(self, *args, **options) -> None:
        errors = []
        if self.download_settings_model.get().download:
            logins = self.log_in_settings_model.objects.filter(download = True)
            for log_in_settings in logins:
                try:
                    self.before_command(log_in_settings)
                    self.run(log_in_settings)
                    self.after_command(log_in_settings)
                except Exception as error:
                    self.except_command(log_in_settings)
                    errors.append(error)
                finally:
                    self.finally_command(log_in_settings)

            show_errors = False
            if show_errors and errors:
                self.logger.exception("========================================")
                for error in errors:
                    self.logger.exception("----------------------------------------")
                    self.logger.exception(type(error))
                    self.logger.exception(error)
                    self.logger.exception("----------------------------------------")
                self.logger.exception("========================================")
                raise DownloadException from errors[0]

    def before_command(self, log_in_settings: models.LogInSettingsModel) -> None:
        self.prepare_chrome_driver()

    def after_command(self, log_in_settings: models.LogInSettingsModel) -> None:
        pass

    def except_command(self, log_in_settings: models.LogInSettingsModel) -> None:
        pass

    def finally_command(self, log_in_settings: models.LogInSettingsModel) -> None:
        if hasattr(self, "driver"):
            try:
                self.driver.close()
                self.driver.quit()
            except WebDriverException as exception:
                if "disconnected" in exception.msg:
                    pass

    def prepare_chrome_driver(self) -> None:
        print(1)
        driver_options = ChromeOptions()
        # этот параметр тоже нужен, так как в режиме headless с некоторыми элементами нельзя взаимодействовать
        driver_options.add_argument("--no-sandbox")
        driver_options.add_argument("--disable-blink-features=AutomationControlled")
        if hasattr(self, "parsing_settings_model") and not self.parsing_settings_model.get().show_browser:
            driver_options.add_argument("--headless")
            driver_options.add_argument("--disable-gpu")
        driver_options.add_argument("--window-size=1920,1080")
        if self.use_chrome_profile:
            driver_options.add_argument(f"--user-data-dir={self.settings.CHROME_PROFILE_FOLDER}")

        driver_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver_options.add_experimental_option(
            "prefs",
            {"download.default_directory": self.settings.TEMP_DOWNLOAD_FOLDER}
        )

        print(2)
        cache_manager = DriverCacheManager(root_dir = f"{pathlib.Path.cwd()}/webdrivers/{self.settings.APP_NAME}")
        driver_manager = ChromeDriverManager(cache_manager = cache_manager).install()
        driver_service = ChromeService(executable_path = driver_manager)
        print(3)

        self.driver = Chrome(options = driver_options, service = driver_service)
        self.driver.maximize_window()
        print(4)
        self.driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})
        print(5)

    def run(self, log_in_settings: models.LogInSettingsModel) -> None:
        raise NotImplementedError()

    def get_cookies_path(self, log_in_settings: models.LogInSettingsModel) -> str:
        raise NotImplementedError()
