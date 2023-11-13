from parsing_helper.web_elements import ExtendedWebElement

from pages import base_page


# https://www.eisz.kz/login
class LogInPage(base_page.BasePage):
    path = "login"

    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.iin_input = ExtendedWebElement(self, '//input[@id = "UserName"]')
        self.password_input = ExtendedWebElement(self, '//input[@id = "Password"]')
        self.enter_button = ExtendedWebElement(self, '//button[@type = "submit" and contains(@class, "primary")]')

    def log_in(self, iin: int, password: str) -> None:
        self.iin_input.send_keys(str(iin))
        self.password_input.send_keys(password)
        self.enter_button.click()
