from selenium.common import WebDriverException

from core.management.commands import core_browser_command


class Command(core_browser_command.CoreBrowserCommand):
    use_chrome_profile = True

    def handle(self, *args, **options) -> None:
        try:
            self.prepare_chrome_driver()
            input("Нажмите ввод (Enter) когда закончите работу с браузером.\n")
            print("Браузер закрывается.")
        finally:
            if hasattr(self, "driver"):
                try:
                    self.driver.close()
                    self.driver.quit()
                except WebDriverException as exception:
                    if "disconnected" in exception.msg:
                        pass
