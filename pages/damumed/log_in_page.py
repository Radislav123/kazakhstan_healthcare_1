from parsing_helper.web_elements import ExtendedWebElement

from pages.damumed import base_page
from damumed import models


# https://pvd.dmed.kz/Authentication/Authentication/SignIn
class LogInPage(base_page.BasePage):
    path = "Authentication/Authentication/SignIn"

    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.login_input = ExtendedWebElement(self, '//input[@id = "tbUserName"]')
        self.password_input = ExtendedWebElement(self, '//input[@id = "tbPassword"]')
        self.enter_button = ExtendedWebElement(self, '//button[@id = "btn-sign-in"]')

    def log_in(self, log_in_settings: models.LogInSettings) -> None:
        self.open()

        self.login_input.send_keys(log_in_settings.login)
        self.password_input.send_keys(log_in_settings.password)

        self.enter_button.click()
