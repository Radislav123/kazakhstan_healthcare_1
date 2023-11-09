import pathlib

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager

from parser import models
from parser.management.commands import parser_command


class Command(parser_command.ParserCommand):
    driver: Chrome
    parsing_settings: models.ParsingSettings

    def handle(self, *args, **options) -> None:
        try:
            self.before_parsing()
            self.run()
        finally:
            self.after_parsing()

    def prepare_driver(self) -> None:
        driver_options = ChromeOptions()
        # этот параметр тоже нужен, так как в режиме headless с некоторыми элементами нельзя взаимодействовать
        driver_options.add_argument("--no-sandbox")
        driver_options.add_argument("--disable-blink-features=AutomationControlled")
        if not self.parsing_settings.show_browser:
            driver_options.add_argument("--headless")
        driver_options.add_argument("--window-size=1920,1080")
        driver_options.add_experimental_option("excludeSwitches", ["enable-logging"])

        cache_manager = DriverCacheManager(root_dir = f"{pathlib.Path.cwd()}/webdrivers/{self.settings.APP_NAME}")
        driver_manager = ChromeDriverManager(cache_manager = cache_manager).install()
        driver_service = Service(executable_path = driver_manager)

        self.driver = Chrome(options = driver_options, service = driver_service)
        self.driver.maximize_window()
        self.driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})

    def before_parsing(self) -> None:
        self.parsing_settings = models.ParsingSettings.get()
        self.prepare_driver()

    def after_parsing(self) -> None:
        self.driver.quit()

    def run(self) -> None:
        pass
