from parsing_helper.pages import base_page
from parsing_helper.web_elements import ExtendedWebElement

from parser.settings import Settings


# https://reports.eisz.kz/
class ReportsBasePage(base_page.BasePage):
    settings = Settings()
    scheme = "https"
    domain = "reports.eisz.kz"

    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.loader = ExtendedWebElement(self, '//div[@aria-hidden = "true"]')
