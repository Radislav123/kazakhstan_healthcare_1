from parsing_helper import settings as helper_settings

from .apps import ParserConfig


class Settings(helper_settings.Settings):
    APP_NAME = ParserConfig.name

    def __init__(self):
        super().__init__()
