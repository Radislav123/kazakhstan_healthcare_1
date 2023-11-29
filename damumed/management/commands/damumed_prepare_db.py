from core.management.commands import core_prepare_db_command
from damumed import models
from damumed.management.commands import damumed_command


class Command(damumed_command.DamumedCommand, core_prepare_db_command.CorePrepareDBCommand):
    download_settings_model = models.DownloadSettings
    log_in_settings_model = models.LogInSettings
    parsing_settings_model = models.ParsingSettings
    report_model = models.Report

    def prepare_db(self) -> None:
        super().prepare_db()
        self.prepare_several_objects(self.settings.secrets.screening_reports, models.ScreeningReport)
        self.prepare_several_objects(self.settings.secrets.unloading_reports, models.UnloadingReport)
