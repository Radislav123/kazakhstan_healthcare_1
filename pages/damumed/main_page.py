from parsing_helper.web_elements import ExtendedWebElement
from selenium.common import TimeoutException

from pages.damumed import base_page


# https://pvd.dmed.kz/
class MainPage(base_page.BasePage):
    path = ""

    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.log_out_button = ExtendedWebElement(self, '//span[@class = "glyphicon glyphicon-off"]')

    def log_out(self) -> None:
        self.open()

        try:
            self.log_out_button.click()
        except TimeoutException:
            pass
