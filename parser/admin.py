from parsing_helper import admin as helper_admin

from parser import models


class BaseAdmin(helper_admin.BaseAdmin):
    model = models.BaseModel


class DownloadSettingsAdmin(BaseAdmin):
    model = models.DownloadSettings


class LogInSettingsAdmin(BaseAdmin):
    model = models.LogInSettings
    not_required_fields = {"folder", }


class ParsingSettingsAdmin(BaseAdmin):
    model = models.ParsingSettings


class ReportAdmin(BaseAdmin):
    model = models.Report
    not_required_fields = set(f"step_{x}" for x in range(1, 8))
    not_required_fields.add("folder")


model_admins_to_register = [DownloadSettingsAdmin, LogInSettingsAdmin, ParsingSettingsAdmin, ReportAdmin]
helper_admin.register_models(model_admins_to_register)
