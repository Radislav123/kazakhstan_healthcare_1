from parsing_helper.web_elements import ExtendedWebElement
from selenium.common import TimeoutException

from pages.damumed import base_page


# https://pvd.dmed.kz/
class MainPage(base_page.BasePage):
    path = ""

    class ModulesOverlay(ExtendedWebElement):
        def __init__(self, page: "MainPage", xpath: str):
            super().__init__(page, xpath)

    class TopBar(ExtendedWebElement):

        def __init__(self, page: "MainPage", xpath: str):
            super().__init__(page, xpath)

            self.modules_button = ExtendedWebElement(self.page, f'{self.xpath}/li[@class = "auth-service"]')

    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.log_out_button = ExtendedWebElement(self, '//span[@class = "glyphicon glyphicon-off"]')
        self.top_bar = self.TopBar(self, '//ul[@class = "nav navbar-nav navbar-left"]')
        self.modules_overlay = self.ModulesOverlay(self, '//div[@id = "module-navigation"]')

    def log_out(self) -> None:
        self.open()

        try:
            self.log_out_button.click()
        except TimeoutException:
            pass
