import time

from parsing_helper.web_elements import ExtendedWebElement
from selenium.webdriver import Chrome

from damumed import models
from pages.damumed import base_page


# https://pvd.dmed.kz/prophylaxis/ScreeningCandidateJournal
class ScreeningsPage(base_page.BasePage):
    path = "prophylaxis/ScreeningCandidateJournal"

    class Filter(ExtendedWebElement):
        def __init__(self, page: "ScreeningsPage", xpath: str):
            super().__init__(page, xpath)

            self.button = ExtendedWebElement(self.page, f'{self.xpath}//span[@role = "button"]/span/..')

        def set_option(self, option: str) -> None:
            option = ExtendedWebElement(self.page, f'//li[@role = "option" and contains(text(), "{option}")]')
            option.click()

    class AgeFilter(ExtendedWebElement):
        def __init__(self, page: "ScreeningsPage", xpath: str):
            super().__init__(page, xpath)

            self.from_input = ExtendedWebElement(self.page, f'{self.xpath}//span[1]/span/input')
            self.to_input = ExtendedWebElement(self.page, f'{self.xpath}//span[2]/span/input')

        def set(self, report: models.Screening) -> None:
            self.from_input.send_keys(str(report.from_age))
            self.to_input.send_keys(str(report.to_age))

    def __init__(self, driver: Chrome, domain: str) -> None:
        super().__init__(driver, domain)

        # noinspection SpellCheckingInspection
        self.filters_button = ExtendedWebElement(self, '//a[@id = "btnScreeningCandidateJouranlFilter"]')
        self.export_to_excel = ExtendedWebElement(self, '//a[@id= "btnExportToExcel"]')
        self.age_filter = self.AgeFilter(self, '//div[@class = "input-group"]/label[text() = "Возраст: от"]/..')
        self.apply_button = ExtendedWebElement(self, '//button[@class = "btn btn-default" and @onclick]')
        self.alert_close_button = ExtendedWebElement(self, '//div[contains(@class, "alert")]/button')

    def set_filters(self, report: models.Screening) -> None:
        for i in range(1, 11):
            time.sleep(1)
            filter_title = report.get_filter_title(i)
            filter_value = report.get_filter_value(i)
            if filter_title and filter_value:
                filter_element = self.Filter(
                    self,
                    f'//div[@class = "input-group"]/*[contains(text(), "{filter_title}")]/..'
                )
                filter_element.button.click()
                filter_element.set_option(filter_value)

    def set_checkboxes(self, report: models.Screening) -> None:
        for i in range(1, 11):
            checkbox_title = report.get_checkbox_title(i)
            if checkbox_title:
                checkbox = ExtendedWebElement(
                    self,
                    f'//label[@class = "k-checkbox-label" and contains(text(), "{checkbox_title}")]'
                )
                checkbox.click()

    def download_report(self) -> None:
        self.apply_button.click()
        self.export_to_excel.click()
