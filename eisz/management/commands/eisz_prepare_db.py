from core.management.commands import core_prepare_db_command
from eisz import models
from eisz.management.commands import eisz_command


class Command(eisz_command.EISZCommand, core_prepare_db_command.CorePrepareDBCommand):
    download_settings_model = models.DownloadSettings
    log_in_settings_model = models.LogInSettings
    parsing_settings_model = models.ParsingSettings
    report_model = models.Report
