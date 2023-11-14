import json
import os
import pathlib
import shutil
import time
from pathlib import Path

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager

from pages import LogInPage, ReportsLogInPage, ReportsPage
from parser import models
from parser.management.commands import parser_command


class DownloadNotFinishedException(Exception):
    pass


# todo: merge download and log_in
class Command(parser_command.ParserCommand):
    driver: Chrome

    def handle(self, *args, **options) -> None:
        try:
            self.before_command()
            self.run()
        finally:
            self.after_command()

    def before_command(self) -> None:
        self.prepare_driver()

    def after_command(self) -> None:
        if hasattr(self, "driver"):
            self.driver.close()
            self.driver.quit()

    def prepare_driver(self) -> None:
        parsing_settings = models.ParsingSettings.get()

        driver_options = ChromeOptions()
        # этот параметр тоже нужен, так как в режиме headless с некоторыми элементами нельзя взаимодействовать
        driver_options.add_argument("--no-sandbox")
        driver_options.add_argument("--disable-blink-features=AutomationControlled")
        if not parsing_settings.show_browser:
            driver_options.add_argument("--headless")
        driver_options.add_argument("--window-size=1920,1080")
        driver_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver_options.add_experimental_option(
            "prefs",
            {"download.default_directory": self.settings.TEMP_DOWNLOAD_FOLDER}
        )

        cache_manager = DriverCacheManager(root_dir = f"{pathlib.Path.cwd()}/webdrivers/{self.settings.APP_NAME}")
        driver_manager = ChromeDriverManager(cache_manager = cache_manager).install()
        driver_service = Service(executable_path = driver_manager)

        self.driver = Chrome(options = driver_options, service = driver_service)
        self.driver.maximize_window()
        self.driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})

    def wait_download(self) -> None:
        download_settings = models.DownloadSettings.get()
        for timer in range(download_settings.max_download_waiting):
            time.sleep(download_settings.download_check_period)
            for file in os.listdir(self.settings.TEMP_DOWNLOAD_FOLDER):
                if file.endswith(".tmp"):
                    break
            else:
                break
        else:
            raise DownloadNotFinishedException()

    def move(self, report: models.Report) -> None:
        files = {os.path.getctime(file): file for file in
                 (f"{self.settings.TEMP_DOWNLOAD_FOLDER}/{x}" for x in os.listdir(self.settings.TEMP_DOWNLOAD_FOLDER))}
        last_file: str = files[max(files)]
        folder = Path(f"{models.DownloadSettings.get().folder}/{report.folder}")
        Path(folder).mkdir(parents = True, exist_ok = True)
        os.replace(last_file, f"{folder}/{report.name}.{last_file.split('.')[-1]}")

    def run(self) -> None:
        log_in_page = LogInPage(self.driver)
        with open(self.settings.AUTH_COOKIES_PATH) as file:
            cookies = json.load(file)
            log_in_page.set_cookies(cookies)

        reports_log_in_page = ReportsLogInPage(self.driver)
        reports_log_in_page.log_in()

        for report in models.Report.objects.filter(download = True):
            reports_page = ReportsPage(self.driver)
            reports_page.open_report(report)
            reports_page.form_button.click()
            try:
                reports_page.format_selector.click()
            except TimeoutException:
                reports_page.form_button.reset()
                reports_page.form_button.click()
                reports_page.format_selector.click()
            reports_page.form_option.click()
            reports_page.download_button.click()
            self.wait_download()
            self.move(report)

        if self.settings.CLEAR_TEMP_DOWNLOAD_FOLDER:
            shutil.rmtree(self.settings.TEMP_DOWNLOAD_FOLDER)
