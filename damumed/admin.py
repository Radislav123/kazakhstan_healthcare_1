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
    not_required_fields = ("folder",)


model_admins_to_register = [DownloadSettingsAdmin, LogInSettingsAdmin, ParsingSettingsAdmin, ReportAdmin]
helper_admin.register_models(model_admins_to_register)
