from typing import TYPE_CHECKING

from parsing_helper import secret_keeper


if TYPE_CHECKING:
    from parser.settings import Settings


class SecretKeeper(secret_keeper.SecretKeeper):
    Module = secret_keeper.SecretKeeper.Module

    class Database(Module):
        ENGINE: str
        NAME: str

    class Django(Module):
        secret_key: str

    database: Database
    django: Django

    def __init__(self, settings: "Settings") -> None:
        super().__init__()
        self.add_module("database", settings.DATABASE_CREDENTIALS_PATH)
        self.add_module("django", settings.DJANGO_CREDENTIALS_PATH)
