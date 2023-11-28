from parsing_helper import admin as helper_admin

from core import admin as core_admin
from damumed import models


class DamumedAdmin(core_admin.CoreAdmin):
    model = models.DamumedModel


class DownloadSettingsAdmin(DamumedAdmin):
    model = models.DownloadSettings


class LogInSettingsAdmin(DamumedAdmin):
    model = models.LogInSettings
    not_required_fields = {"folder", "download_duration"}


class ParsingSettingsAdmin(DamumedAdmin):
    model = models.ParsingSettings


class ReportAdmin(DamumedAdmin):
    model = models.Report
    not_required_fields = {"folder", }


class ScreeningReportAdmin(DamumedAdmin):
    model = models.ScreeningReport
    not_required_fields = {"folder", "from_age", "to_age"}
    not_required_fields.update(f"filter_title_{x}" for x in range(1, 11))
    not_required_fields.update(f"filter_value_{x}" for x in range(1, 11))
    not_required_fields.update(f"checkbox_title_{x}" for x in range(1, 11))


model_admins_to_register = [
    DownloadSettingsAdmin,
    LogInSettingsAdmin,
    ParsingSettingsAdmin,
    ReportAdmin,
    ScreeningReportAdmin
]
helper_admin.register_models(model_admins_to_register)
