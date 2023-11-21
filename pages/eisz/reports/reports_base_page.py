from parsing_helper.web_elements import ExtendedWebElement

from pages.eisz import base_page


# https://reports.eisz.kz/
class ReportsBasePage(base_page.BasePage):
    domain = "reports.eisz.kz"

    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.loader_hidden = ExtendedWebElement(self, '//div[@aria-hidden = "true"]')
        self.loader_visible = ExtendedWebElement(self, '//div[@aria-hidden = "false"]')
        self.title = ExtendedWebElement(self, '//h1')
