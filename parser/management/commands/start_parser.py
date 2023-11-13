import pathlib

from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.firefox.service import Service
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.firefox import GeckoDriverManager

from parser import models
from parser.management.commands import parser_command


class Command(parser_command.ParserCommand):
    driver: Firefox
    parsing_settings: models.ParsingSettings

    def handle(self, *args, **options) -> None:
        try:
            self.before_parsing()
            self.run()
        finally:
            self.after_parsing()

    def prepare_driver(self) -> None:
        driver_options = FirefoxOptions()
        if not self.parsing_settings.show_browser:
            driver_options.add_argument("--headless")
        driver_options.add_argument("--window-size=1920,1080")

        cache_manager = DriverCacheManager(root_dir = f"{pathlib.Path.cwd()}/webdrivers/{self.settings.APP_NAME}")
        driver_manager = GeckoDriverManager(cache_manager = cache_manager).install()
        driver_service = Service(
            executable_path = driver_manager,
            log_path = f"{self.settings.LOG_FOLDER}/geckodriver.log"
        )

        self.driver = Firefox(options = driver_options, service = driver_service)
        self.driver.maximize_window()

    def before_parsing(self) -> None:
        self.parsing_settings = models.ParsingSettings.get()
        self.prepare_driver()

    def after_parsing(self) -> None:
        self.driver.quit()

    def run(self) -> None:
        pass
