import json
import pathlib

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager

from pages import LogInPage
from parser.management.commands import parser_command


class Command(parser_command.ParserCommand):
    help = "Открывает окно авторизации"
    driver: Chrome

    def handle(self, *args, **options):
        try:
            self.before_command()
            self.log_in()
        finally:
            self.after_command()

    def prepare_driver(self) -> None:
        options = ChromeOptions()

        options.add_argument("--no-sandbox")
        cache_manager = DriverCacheManager(
            root_dir = f"{pathlib.Path.cwd()}/webdrivers/{self.settings.APP_NAME}/log_in_window"
        )
        driver_manager = ChromeDriverManager(cache_manager = cache_manager).install()
        service = Service(executable_path = driver_manager)

        self.driver = Chrome(options = options, service = service)
        self.driver.maximize_window()

    # todo: remove method?
    # todo: remove LOG_IN_DRIVER_DATA_PATH?
    def write_driver_info(self, driver: Chrome) -> None:
        with open(self.settings.LOG_IN_DRIVER_DATA_PATH, 'w') as file:
            # noinspection PyProtectedMember
            json.dump({"url": driver.command_executor._url, "session_id": driver.session_id}, file, indent = 4)

    def log_in(self) -> None:
        page = LogInPage(self.driver)
        page.open()
        page.log_in(self.settings.secrets.log_in_settings.iin, self.settings.secrets.log_in_settings.password)
        input("Нажмите ввод (enter) после выбора ЕЦП.")
        self.write_driver_info(self.driver)
        with open(self.settings.AUTH_COOKIES_PATH, 'w') as file:
            json.dump(self.driver.get_cookies(), file, indent = 4)

    def before_command(self) -> None:
        self.prepare_driver()

    def after_command(self) -> None:
        if hasattr(self, "driver"):
            self.driver.quit()
