from parsing_helper.web_elements import ExtendedWebElement

from pages import base_page
from parser import models


# https://www.eisz.kz/default.aspx
class ReportsPage(base_page.BasePage):
    path = "default.aspx"

    def __init__(self, driver) -> None:
        super().__init__(driver)

    def open_report(self, report_path: models.ReportPath) -> None:
        for i in range(1, 10):
            step_path = report_path.get_step_path(i)
            if step_path is not None:
                step_element = ExtendedWebElement(self, f'//td[text() = "{step_path}"]')
                step_element.click()
            else:
                break
