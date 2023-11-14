from parsing_helper.web_elements import ExtendedWebElement

from pages import base_page


# https://www.eisz.kz/edslogin
class DigitalLogInPage(base_page.BasePage):
    path = "edslogin"

    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.enter_button = ExtendedWebElement(self, '//button[@id = "edsLoginBtn"]')
        self.choose_certificate_button = ExtendedWebElement(self, '//button[@onclick]')

    def log_in(self) -> None:
        # не надо открывать страницу, так как это сбрасывает ввод ЭЦП
        # self.open()
        self.choose_certificate_button.click()
        self.enter_button.click()
