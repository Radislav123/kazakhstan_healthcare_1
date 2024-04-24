from parsing_helper.pages import base_page
from selenium.webdriver import Chrome

from damumed.settings import Settings


# https://pvd.dmed.kz/
class BasePage(base_page.BasePage):
    settings = Settings()
    scheme = "https"

    def __init__(self, driver: Chrome, domain: str) -> None:
        super().__init__(driver)
        self.domain = domain
