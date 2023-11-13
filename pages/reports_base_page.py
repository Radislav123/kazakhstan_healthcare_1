from parsing_helper.pages import base_page


# https://reports.eisz.kz/
class ReportsBasePage(base_page.BasePage):
    scheme = "https"
    domain = "reports.eisz.kz"
