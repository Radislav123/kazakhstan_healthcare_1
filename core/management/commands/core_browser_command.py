import pathlib

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.firefox import GeckoDriverManager
from typing import Type

from core import models
from core.management.commands import core_command


class DownloadException(Exception):
    pass


class CoreBrowserCommand(core_command.CoreCommand):
    log_in_settings_model: Type[models.LogInSettingsModel]
    parsing_settings_model: Type[models.ParsingSettingsModel]
    driver: Chrome

    def handle(self, *args, **options) -> None:
        errors = []
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

        if errors:
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
        parsing_settings = self.parsing_settings_model.get()

        driver_options = ChromeOptions()
        # этот параметр тоже нужен, так как в режиме headless с некоторыми элементами нельзя взаимодействовать
        driver_options.add_argument("--no-sandbox")
        driver_options.add_argument("--disable-blink-features=AutomationControlled")
        if not parsing_settings.show_browser:
            driver_options.add_argument("--headless")
            driver_options.add_argument("--disable-gpu")
        driver_options.add_argument("--window-size=1920,1080")
        driver_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver_options.add_experimental_option(
            "prefs",
            {"download.default_directory": self.settings.TEMP_DOWNLOAD_FOLDER}
        )

        cache_manager = DriverCacheManager(root_dir = f"{pathlib.Path.cwd()}/webdrivers/{self.settings.APP_NAME}")
        driver_manager = ChromeDriverManager(cache_manager = cache_manager).install()
        driver_service = ChromeService(executable_path = driver_manager)

        self.driver = Chrome(options = driver_options, service = driver_service)
        self.driver.maximize_window()
        self.driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})

    def prepare_firefox_driver(self) -> None:
        parsing_settings = self.parsing_settings_model.get()

        driver_options = FirefoxOptions()
        if not parsing_settings.show_browser:
            driver_options.add_argument("--headless")
        driver_options.add_argument("--width=1920")
        driver_options.add_argument("--height=1080")
        driver_options.set_preference("browser.download.dir", self.settings.TEMP_DOWNLOAD_FOLDER)
        driver_options.set_preference("javascript.enabled", True)
        driver_options.set_preference("dom.serviceWorkers.enabled", True)

        cache_manager = DriverCacheManager(root_dir = f"{pathlib.Path.cwd()}/webdrivers/{self.settings.APP_NAME}")
        driver_manager = GeckoDriverManager(cache_manager = cache_manager).install()
        driver_service = FirefoxService(executable_path = driver_manager)

        self.driver = Firefox(
            options = driver_options,
            service = driver_service,
            # todo: местоположение не меняется, хотя должно
            log_path = f"{self.settings.LOG_FOLDER}/geckodriver.log"
        )
        self.driver.maximize_window()

    def run(self, log_in_settings: models.LogInSettingsModel) -> None:
        raise NotImplementedError()

    def get_cookies_path(self, log_in_settings: models.LogInSettingsModel) -> str:
        raise NotImplementedError()
