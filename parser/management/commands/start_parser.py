import json
import pathlib
import time

from parsing_helper.web_elements import ExtendedWebElement
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager

from pages import LogInPage, ReportsLogInPage, ReportsPage
from parser import models
from parser.management.commands import parser_command


class Command(parser_command.ParserCommand):
    driver: Chrome
    parsing_settings: models.ParsingSettings

    def handle(self, *args, **options) -> None:
        try:
            self.before_command()
            self.run()
        finally:
            self.after_command()

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

    def before_command(self) -> None:
        self.parsing_settings = models.ParsingSettings.get()
        self.prepare_driver()

    def after_command(self) -> None:
        if hasattr(self, "driver"):
            self.driver.quit()

    def run(self) -> None:
        log_in_page = LogInPage(self.driver)
        with open(self.settings.AUTH_COOKIES_PATH) as file:
            cookies = json.load(file)
            log_in_page.set_cookies(cookies)

        reports_log_in_page = ReportsLogInPage(self.driver)
        reports_log_in_page.log_in()

        reports_page = ReportsPage(self.driver)
        reports_page.open()
        time.sleep(3)
        checker = ExtendedWebElement(reports_page, '//h1[contains(text(), "Ошибка сервера в приложении")]')
        try:
            checker.init()
        except TimeoutException:
            pass
        else:
            self.driver.back()

        input()
