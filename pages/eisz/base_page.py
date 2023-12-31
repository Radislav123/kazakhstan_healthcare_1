from parsing_helper.pages import base_page

from eisz.settings import Settings


# https://www.eisz.kz/
class BasePage(base_page.BasePage):
    settings = Settings()
    scheme = "https"
    domain = "www.eisz.kz"
