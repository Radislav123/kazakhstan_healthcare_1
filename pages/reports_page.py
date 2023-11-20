import time

from parsing_helper.web_elements import ExtendedWebElement
from selenium.common import TimeoutException

from pages import reports_base_page
from parser import models


class FormButtonNotClickedException(Exception):
    pass


class PageNotReopened(Exception):
    pass


# https://www.eisz.kz/default.aspx
class ReportsPage(reports_base_page.ReportsBasePage):
    path = "default.aspx"
    translate = 'translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")'
    translate_value = 'translate(@value, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")'
    translate_text = 'translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")'

    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.form_button = ExtendedWebElement(self, '//div[@class = "dxb"]')

        self.format_selector = ExtendedWebElement(self, '//select[contains(@name, "MainContent")]')
        self.format_option = ExtendedWebElement(
            self,
            f'//option[contains({self.translate}, "{models.DownloadSettings.get().format.lower()}")]'
        )
        self.download_button = ExtendedWebElement(self, '//input[contains(@id, "Save")]')

        self.begin_date_input = ExtendedWebElement(
            self,
            '//input[contains(@name, "calBeginDate") and not(@type = "hidden")]'
        )
        self.end_date_input = ExtendedWebElement(
            self,
            '//input[contains(@name, "calEndDate") and not(@type = "hidden")]'
        )

    def check_open_error(self) -> None:
        time.sleep(3)
        checker = ExtendedWebElement(self, '//h1[contains(text(), "Ошибка сервера в приложении")]')
        try:
            checker.init()
        except TimeoutException:
            pass
        else:
            self.driver.back()

    def open(self) -> None:
        counter = 5
        while True:
            super().open()
            self.check_open_error()
            try:
                self.form_button.init()
                self.form_button.reset()
                counter -= 1
                if counter <= 0:
                    raise PageNotReopened()
                time.sleep(self.settings.SELENIUM_DEFAULT_TIMEOUT)
            except TimeoutException:
                break

    def open_report(self, report: models.Report) -> None:
        self.open()

        for i in range(1, 8):
            step_path = report.get_step_path(i)
            if step_path:
                step_element = ExtendedWebElement(self, f'//td[text() = "{step_path.strip()}"]')
                step_element.click()
            else:
                break

    def set_period(self) -> None:
        # ожидание прогрузки страницы
        self.form_button.init(self.form_button.WaitCondition.CLICKABLE)
        self.form_button.reset()

        download_settings = models.DownloadSettings.get()
        begin_date_string = download_settings.begin_date.strftime(self.settings.DOWNLOAD_DATE_FORMAT)
        end_date_string = download_settings.end_date.strftime(self.settings.DOWNLOAD_DATE_FORMAT)
        begin_on_change = "aspxETextChanged('MainContent_ASPxSplitter1_viewer_reportCriteria_psCriteria_calBeginDate')"
        end_on_change = "aspxETextChanged('MainContent_ASPxSplitter1_viewer_reportCriteria_psCriteria_calEndDate')"

        self.driver.execute_script(
            f"arguments[0].setAttribute('value','{begin_date_string}');\n"
            f"{begin_on_change};",
            self.begin_date_input.selenium_element
        )
        self.driver.execute_script(
            f"arguments[0].setAttribute('value','{end_date_string}');\n"
            f"{end_on_change};",
            self.end_date_input.selenium_element
        )

    def set_filters(self, report: models.Report) -> None:
        for i in range(1, 11):
            filter_title = report.get_filter_title(i)
            filter_value = report.get_filter_value(i)
            if filter_title and filter_value:
                filter_element = ExtendedWebElement(
                    self,
                    # filter_title.lower().strip() - не работает
                    f'//span[contains({self.translate}, "{filter_title.strip()}")]/../..'
                )
                open_options_button = ExtendedWebElement(
                    self,
                    f'{filter_element.xpath}//td[contains(@class, "Button")]'
                )
                option = ExtendedWebElement(
                    self,
                    # filter_title.value().strip() - не работает
                    f'{filter_element.xpath}//td[contains({self.translate_text}, "{filter_value.strip()}")]'
                )

                open_options_button.click()
                checker = ExtendedWebElement(
                    self,
                    f'{filter_element.xpath}//input[contains({self.translate_value}, "{filter_value.strip()}")]'
                )
                counter = 5
                while True:
                    try:
                        time.sleep(1)
                        option.click()
                        checker.init()
                        break
                    except TimeoutException as exception:
                        option.reset()
                        counter -= 1
                        if counter <= 0:
                            raise exception

    def download_report(self) -> None:
        counter = 5
        while True:
            try:
                self.form_button.click()
                self.loader_visible.init()
                break
            except TimeoutException as exception:
                self.form_button.reset()
                counter -= 1
                if counter <= 0:
                    raise exception

        counter = 20 * 60 // self.settings.SELENIUM_DEFAULT_TIMEOUT
        while True:
            try:
                self.loader_hidden.reset()
                self.loader_hidden.init()
                break
            except TimeoutException as exception:
                counter -= 1
                if counter <= 0:
                    raise exception

        self.format_selector.click()
        self.format_option.click()
        self.download_button.click()
