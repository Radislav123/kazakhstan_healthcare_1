import time

from parsing_helper.web_elements import ExtendedWebElement

from pages.eisz import base_page


# https://www.eisz.kz/
class MainPage(base_page.BasePage):
    path = ""

    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.profile_button = ExtendedWebElement(self, '//a[@data-toggle]')
        self.exit_button = ExtendedWebElement(self, '//a[@id = "exitLink"]')

    def log_out(self) -> None:
        self.open()
        time.sleep(1)
        self.profile_button.click()
        time.sleep(1)
        self.exit_button.click()
        timer = 5
        for i in range(timer):
            if self.driver.current_url != "https://www.eisz.kz/login?ReturnUrl=%2F":
                time.sleep(1)
            else:
                break
