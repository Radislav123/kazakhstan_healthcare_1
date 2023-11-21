from core.management.commands import core_command
from eisz import settings


class EISZCommand(core_command.CoreCommand):
    settings = settings.Settings()
