from core.management.commands import core_command
from damumed import settings


class DamumedCommand(core_command.CoreCommand):
    settings = settings.Settings()
