import time

from parsing_helper.web_elements import ExtendedWebElement
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from pages import base_page
from parser import models


# https://www.eisz.kz/default.aspx
class ReportsPage(base_page.BasePage):
    path = "default.aspx"

    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.form_button = ExtendedWebElement(self, '//div[@class = "dxb"]')

        self.format_selector = ExtendedWebElement(self, '//select[contains(@name, "MainContent")]')
        self.format_selector.wait = WebDriverWait(self.driver, self.settings.SELENIUM_DEFAULT_TIMEOUT * 20)
        translate = 'translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz")'
        self.form_option = ExtendedWebElement(
            self,
            f'//option[contains({translate}, "{models.DownloadSettings.get().format.lower()}")]'
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

    def open_report(self, report: models.Report) -> None:
        self.open()
        for i in range(1, 10):
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
