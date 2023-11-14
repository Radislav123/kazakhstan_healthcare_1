import json
import pathlib

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager

from pages import DigitalLogInPage, LogInPage
from parser.management.commands import parser_command


class Command(parser_command.ParserCommand):
    help = "Открывает окно для авторизации на сайте"
    driver: Chrome

    def handle(self, *args, **options):
        try:
            self.before_command()
            self.log_in()
        finally:
            self.after_command()

    def prepare_driver(self) -> None:
        options = ChromeOptions()

        cache_manager = DriverCacheManager(
            root_dir = f"{pathlib.Path.cwd()}/webdrivers/{self.settings.APP_NAME}/log_in_window"
        )
        driver_manager = ChromeDriverManager(cache_manager = cache_manager).install()
        service = Service(executable_path = driver_manager)

        self.driver = Chrome(options = options, service = service)
        self.driver.maximize_window()

    def log_in(self) -> None:
        log_in_page = LogInPage(self.driver)
        log_in_page.log_in(self.settings.secrets.log_in_settings.iin, self.settings.secrets.log_in_settings.password)

        input_text = ["Нажмите ввод (enter) после выбора ЕЦП.",
                      "Не закрывайте браузер, он должен закрыться сам после ввода (enter).\n"]
        # todo: remove input
        input(' '.join(input_text))
        digital_log_in_page = DigitalLogInPage(self.driver)
        digital_log_in_page.log_in()

        with open(self.settings.AUTH_COOKIES_PATH, 'w') as file:
            json.dump(self.driver.get_cookies(), file, indent = 4)

    def before_command(self) -> None:
        self.prepare_driver()

    def after_command(self) -> None:
        if hasattr(self, "driver"):
            self.driver.close()
            self.driver.quit()
