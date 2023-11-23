from parsing_helper.django_commands import create_admin

from core.management.commands import core_command


class Command(core_command.CoreCommand, create_admin.CreateAdminCommand):
    pass
