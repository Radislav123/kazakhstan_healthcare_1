from typing import TYPE_CHECKING

from parsing_helper import secret_keeper


if TYPE_CHECKING:
    from parser.settings import Settings


class SecretKeeper(secret_keeper.SecretKeeper):
    Module = secret_keeper.SecretKeeper.Module

    def __init__(self, settings: "Settings") -> None:
        super().__init__(settings)
