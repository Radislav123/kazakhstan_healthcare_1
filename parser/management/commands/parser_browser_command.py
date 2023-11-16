import pathlib

from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.firefox import GeckoDriverManager

from parser import models
from parser.management.commands import parser_command


class ParserBrowserCommand(parser_command.ParserCommand):
    driver: Chrome

    def handle(self, *args, **options) -> None:
        logins = models.LogInSettings.objects.all()
        for log_in_settings in logins:
            try:
                self.before_command(log_in_settings)
                self.run(log_in_settings)
                self.after_command(log_in_settings)
            except Exception as error:
                self.logger.error(error)
                self.except_command(log_in_settings)
            finally:
                self.finally_command(log_in_settings)

    def before_command(self, log_in_settings: models.LogInSettings) -> None:
        self.prepare_chrome_driver()

    def after_command(self, log_in_settings: models.LogInSettings) -> None:
        pass

    def except_command(self, log_in_settings: models.LogInSettings) -> None:
        pass

    def finally_command(self, log_in_settings: models.LogInSettings) -> None:
        if hasattr(self, "driver"):
            self.driver.close()
            self.driver.quit()

    def prepare_chrome_driver(self) -> None:
        parsing_settings = models.ParsingSettings.get()

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
        parsing_settings = models.ParsingSettings.get()

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

    def run(self, log_in_settings: models.LogInSettings) -> None:
        raise NotImplementedError()

    def get_cookies_path(self, log_in_settings: models.LogInSettings) -> str:
        return self.settings.AUTH_COOKIES_PATH.replace("placeholder", str(log_in_settings.id))
