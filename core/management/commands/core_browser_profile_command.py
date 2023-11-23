import pathlib

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager

from core import models as core_models
from core.management.commands import core_browser_command


class CoreBrowserProfileCommand(core_browser_command.CoreBrowserCommand):
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
        driver_options.add_argument(f"--user-data-dir={self.settings.CHROME_PROFILE_FOLDER}")
        driver_options.add_argument(f"--profile-directory={core_models.CoreSettings.get().chrome_profile_id}")
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
