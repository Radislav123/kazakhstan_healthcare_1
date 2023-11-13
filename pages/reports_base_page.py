from parsing_helper.pages import base_page
from parser.settings import Settings


# https://reports.eisz.kz/
class ReportsBasePage(base_page.BasePage):
    settings = Settings()
    scheme = "https"
    domain = "reports.eisz.kz"
