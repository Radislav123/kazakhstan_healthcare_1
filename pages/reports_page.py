import time

from parsing_helper.web_elements import ExtendedWebElement
from selenium.common import TimeoutException

from pages import base_page
from parser import models


# https://www.eisz.kz/default.aspx
class ReportsPage(base_page.BasePage):
    path = "default.aspx"

    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.form_button = ExtendedWebElement(self, '//div[@class = "dxb"]')

        self.format_selector = ExtendedWebElement(self, '//select[contains(@name, "MainContent")]')
        translate = 'translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz")'
        self.form_option = ExtendedWebElement(
            self,
            f'//option[contains({translate}, "{models.DownloadSettings.get().format.lower()}")]'
        )
        self.download_button = ExtendedWebElement(self, '//input[contains(@id, "Save")]')

    def open_report(self, report: models.Report) -> None:
        self.open()
        for i in range(1, 10):
            step_path = report.get_step_path(i)
            if step_path:
                step_element = ExtendedWebElement(self, f'//td[text() = "{step_path.strip()}"]')
                step_element.click()
            else:
                break

    def download_report(self) -> None:
        self.form_button.click()
        try:
            self.format_selector.click()
        except TimeoutException:
            self.form_button.reset()
            self.form_button.click()
            self.format_selector.click()
        self.form_option.click()
        self.download_button.click()

    def open(self) -> None:
        super().open()
        time.sleep(3)
        checker = ExtendedWebElement(self, '//h1[contains(text(), "Ошибка сервера в приложении")]')
        try:
            checker.init()
        except TimeoutException:
            pass
        else:
            self.driver.back()
