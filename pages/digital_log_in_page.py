from parsing_helper.web_elements import ExtendedWebElement

from pages import base_page


# https://www.eisz.kz/edslogin
class DigitalLogInPage(base_page.BasePage):
    path = "edslogin"

    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.enter_button = ExtendedWebElement(self, '//button[@id = "edsLoginBtn"]')

    def log_in(self) -> None:
        # не надо открывать страницу, так как это сбрасывает ввод ЭЦП
        # self.open()
        self.enter_button.click()
