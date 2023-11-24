from parsing_helper.pages import base_page

from damumed.settings import Settings


# https://pvd.dmed.kz/
class BasePage(base_page.BasePage):
    settings = Settings()
    scheme = "https"
    domain = "pvd.dmed.kz"
