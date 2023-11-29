import copy
import time

from parsing_helper.web_elements import ExtendedWebElement
from selenium.common import ElementClickInterceptedException, TimeoutException

from damumed import models
from pages.damumed import base_page


class TabNotOpenedException(Exception):
    pass


# https://stat-pvd.dmed.kz/report
class ReportsPage(base_page.BasePage):
    domain = "stat-pvd.dmed.kz"
    path = "report"

    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.begin_date_input = ExtendedWebElement(self, '//input[@id = "dtpBeginDate"]')
        self.end_date_input = ExtendedWebElement(self, '//input[@id = "dtpEndDate"]')
        self.form_button = ExtendedWebElement(self, '//button[contains(@onclick, "RegReportGenerate()")]')

    def open_report(self, report: models.Report) -> None:
        self.open()
        step_path = report.get_step_path(1)
        if step_path:
            if step_path:
                step_element = ExtendedWebElement(self, f'//a[contains(text(), "{step_path}")]')
                if "#panelbar-1" not in step_element.selenium_element.get_attribute("href"):
                    step_element.click()

            for i in range(2, 11):
                step_path = report.get_step_path(i)
                if step_path:
                    # noinspection SpellCheckingInspection
                    step_element = ExtendedWebElement(
                        self,
                        f'//td[@role = "gridcell" and contains(text(), "{step_path}")]'
                    )
                    step_element.click()
                else:
                    break

    def set_period(self) -> None:
        download_settings = models.DownloadSettings.get()
        begin_date_string = download_settings.begin_date.strftime(self.settings.DOWNLOAD_DATE_FORMAT)
        end_date_string = download_settings.end_date.strftime(self.settings.DOWNLOAD_DATE_FORMAT)

        counter = self.settings.REPORT_FORM_TIMEOUT // self.settings.SELENIUM_DEFAULT_TIMEOUT
        while True:
            try:
                self.begin_date_input.reset()
                self.begin_date_input.click()
                break
            except ElementClickInterceptedException as exception:
                counter -= 1
                if counter <= 0:
                    raise exception
        self.begin_date_input.selenium_element.clear()
        self.begin_date_input.send_keys(begin_date_string)
        self.end_date_input.click()
        self.end_date_input.selenium_element.clear()
        self.end_date_input.send_keys(end_date_string)

    def set_filters(self, report: models.Report) -> None:
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

    def set_checkbox_filters(self, report: models.Report) -> None:
        for i in range(1, 11):
            filter_title = report.get_checkbox_filter_title(i)
            filter_value = report.get_checkbox_filter_value(i)
            if filter_title and filter_value:
                # noinspection SpellCheckingInspection
                filter_element = ExtendedWebElement(
                    self,
                    f'//div[@class = "row" and @id = "RegServiceRadioBtnsDiv"]'
                    f'/div/label[contains(text(), "{filter_title}")]/../..'
                )
                option = ExtendedWebElement(
                    self,
                    f'{filter_element.xpath}/div/label[contains(text(), "{filter_value}")]'
                )

                option.click()

    def set_multiple_filters(self, report: models.Report) -> None:
        for i in range(1, 11):
            filter_title = report.get_multiple_filter_title(i)
            filter_value = report.get_multiple_filter_value(i)
            if filter_title and filter_value:
                # noinspection SpellCheckingInspection
                filter_element = ExtendedWebElement(
                    self,
                    f'//div[@id = "regTypSrcFinMultiDiv" and @style = "display: block;"]'
                    f'/div/label[contains(text(), "{filter_title}")]/../..'
                )
                option = ExtendedWebElement(
                    self,
                    f'//ul[@aria-hidden = "false"]/li[@role = "option" and contains(text(), "{filter_value}")]'
                )
                try:
                    filter_input = ExtendedWebElement(self, f'{filter_element.xpath}/div/div')

                    filter_input.click()
                    option.click()
                except TimeoutException:
                    filter_input = ExtendedWebElement(self, f'{filter_element.xpath}//ul/li')

                    filter_input.click()
                    option.click()

    def download_report(self) -> None:
        self.form_button.click()

        counter = 1 * 60 // self.settings.SELENIUM_DEFAULT_TIMEOUT
        while len(self.driver.window_handles) < 2 and counter >= 0:
            time.sleep(self.settings.SELENIUM_DEFAULT_TIMEOUT)
        if len(self.driver.window_handles) < 2:
            raise TabNotOpenedException()
        tabs = copy.copy(self.driver.window_handles)
        tabs.remove(self.driver.current_window_handle)
        if len(tabs) > 1:
            raise ValueError()
        self.driver.switch_to.window(tabs[0])

        counter = self.settings.REPORT_FORM_TIMEOUT // self.settings.SELENIUM_DEFAULT_TIMEOUT
        while True:
            try:
                loader = ExtendedWebElement(self, '//div[@id = "MvcViewerReportPanel"]/div')
                loader.init()
                break
            except TimeoutException as exception:
                counter -= 1
                if counter <= 0:
                    raise exception

        save_button = ExtendedWebElement(self, '//td[@id = "MvcViewerButtonSaveCaption"]')
        format_option = ExtendedWebElement(self, '//td[contains(text(), "Microsoft Excel 2007")]')
        confirm_button = ExtendedWebElement(self, '//td[@id = "MvcViewerButtonExportFormOkCaption"]')
        save_button.click()
        format_option.click()
        confirm_button.click()
