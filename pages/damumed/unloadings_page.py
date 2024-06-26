import time

from parsing_helper.web_elements import ExtendedWebElement
from selenium.common import TimeoutException
from selenium.webdriver import Chrome

from damumed import models
from pages.damumed import base_page


# https://stat-pvd.dmed.kz/Unloads
class UnloadingPage(base_page.BasePage):
    path = "Unloads"

    def __init__(self, driver: Chrome, domain: str) -> None:
        super().__init__(driver, f"stat-{domain}")

        self.begin_date_input = ExtendedWebElement(self, '//input[@id = "dtBeginDate"]')
        self.end_date_input = ExtendedWebElement(self, '//input[@id = "dtEndDate"]')
        self.form_button = ExtendedWebElement(self, '//button[contains(@onclick, "getUnload()")]')

        self.loader_hidden = ExtendedWebElement(self, '//body[not(@class = "loading")]')
        self.loader_visible = ExtendedWebElement(self, '//body[@class = "loading"]')

        self.download_start_notification = ExtendedWebElement(self, '//div[@class = "k-notification-wrap"]')
        self.update_last_button = ExtendedWebElement(
            self,
            '//tr[1]/td/div[@class = "cell"]/button/span[text() = "Обновить"]'
        )
        self.download_last_button = ExtendedWebElement(
            self,
            '//tr[1]/td/div[@class = "cell"]/button/span[text() = "Загрузить"]'
        )

    def open_report(self, report: models.Unloading) -> None:
        self.open()
        # на ПК заказчика это необходимо
        time.sleep(3)

        for i in range(1, 11):
            step_path = report.get_step_path(i)
            if step_path:
                step_element = ExtendedWebElement(self, f'//span[text() = "{step_path}"]')
                step_element.click()
            else:
                break

    def set_period(self) -> None:
        download_settings = models.DownloadSettings.get()
        begin_date_string = download_settings.begin_date.strftime(self.settings.DOWNLOAD_DATE_FORMAT)
        end_date_string = download_settings.end_date.strftime(self.settings.DOWNLOAD_DATE_FORMAT)

        self.begin_date_input.click()
        self.begin_date_input.selenium_element.clear()
        self.begin_date_input.send_keys(begin_date_string)
        self.end_date_input.click()
        self.end_date_input.selenium_element.clear()
        self.end_date_input.send_keys(end_date_string)

    def set_filters(self, report: models.Unloading) -> None:
        for i in range(1, 11):
            filter_title = report.get_filter_title(i)
            filter_value = report.get_filter_value(i)
            if filter_title and filter_value:
                filter_element = ExtendedWebElement(self, f'//label[contains(text(), "{filter_title}")]/../..')
                button = ExtendedWebElement(
                    self,
                    f'{filter_element.xpath}/div/span/span/span[@class = "k-select"]'
                )
                option = ExtendedWebElement(
                    self,
                    f'//li[@role = "option" and contains(text(), \'{filter_value}\')]'
                )

                button.click()
                option.click()

    def download_report(self) -> None:
        self.form_button.click()
        self.download_start_notification.init()

        counter = self.settings.REPORT_FORM_TIMEOUT // self.settings.SELENIUM_DEFAULT_TIMEOUT
        while True:
            try:
                self.download_last_button.click()
                break
            except TimeoutException as exception:
                self.update_last_button.click()
                counter -= 1
                if counter <= 0:
                    raise exception
