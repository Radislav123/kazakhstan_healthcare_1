from parsing_helper.web_elements import ExtendedWebElement

from pages.eisz.reports import reports_base_page


# https://www.eisz.kz/Account/Login.aspx
class ReportsLogInPage(reports_base_page.ReportsBasePage):
    path = "Account/Login.aspx"

    def __init__(self, driver) -> None:
        super().__init__(driver)

        self.eta_selector = ExtendedWebElement(self, '//span[@id = "MainContent_rbSystem_RB0_I_D"]')
        self.enter_button = ExtendedWebElement(self, '//div[@id = "MainContent_LoginWithETA_CD"]')

    def log_in(self) -> None:
        self.open()
        self.eta_selector.click()
        self.enter_button.click()
