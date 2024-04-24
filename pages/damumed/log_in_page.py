import time

from parsing_helper.web_elements import ExtendedWebElement
from selenium.webdriver import Chrome

from damumed import models
from pages.damumed import base_page


# https://pvd.dmed.kz/Authentication/Authentication/SignIn
class LogInPage(base_page.BasePage):
    path = "Authentication/Authentication/SignIn"

    def __init__(self, driver: Chrome, domain: str) -> None:
        super().__init__(driver, domain)

        self.login_input = ExtendedWebElement(self, '//input[@id = "tbUserName"]')
        self.password_input = ExtendedWebElement(self, '//input[@id = "tbPassword"]')
        self.enter_button = ExtendedWebElement(self, '//button[@id = "btn-sign-in"]')

    def log_in(self, log_in_settings: models.LogInSettings) -> None:
        self.open()
        # на ПК заказчика это необходимо
        time.sleep(3)

        self.login_input.send_keys(log_in_settings.login)
        self.password_input.send_keys(log_in_settings.password)

        self.enter_button.click()
