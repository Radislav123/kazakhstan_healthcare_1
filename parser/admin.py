from parsing_helper import admin as helper_admin

from parser import models


class BaseAdmin(helper_admin.BaseAdmin):
    model = models.BaseModel


class DownloadSettingsAdmin(BaseAdmin):
    model = models.DownloadSettings


class LogInSettingsAdmin(BaseAdmin):
    model = models.LogInSettings


class ParsingSettingsAdmin(BaseAdmin):
    model = models.ParsingSettings


class ReportPathAdmin(BaseAdmin):
    model = models.ReportPath
    not_required_fields = set(f"step_{x}" for x in range(1, 10))


model_admins_to_register = [DownloadSettingsAdmin, LogInSettingsAdmin, ParsingSettingsAdmin, ReportPathAdmin]
helper_admin.register_models(model_admins_to_register)
