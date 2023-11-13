from parsing_helper.web_elements import ExtendedWebElement

from pages import base_page


# https://www.eisz.kz/default.aspx
class ReportsPage(base_page.BasePage):
    path = "default.aspx"

    def __init__(self, driver) -> None:
        super().__init__(driver)
