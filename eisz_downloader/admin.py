from parsing_helper import admin as helper_admin

from core import admin as core_admin
from eisz_downloader import models


class EISZDownloaderAdmin(core_admin.CoreAdmin):
    model = models.EISZDownloaderModel


class DownloadSettingsAdmin(EISZDownloaderAdmin):
    model = models.DownloadSettings


class LogInSettingsAdmin(EISZDownloaderAdmin):
    model = models.LogInSettings
    not_required_fields = {"folder", "download_duration"}


class ParsingSettingsAdmin(EISZDownloaderAdmin):
    model = models.ParsingSettings


class ReportAdmin(EISZDownloaderAdmin):
    model = models.Report
    not_required_fields = set(f"step_{x}" for x in range(1, 8))
    not_required_fields.update(f"filter_title_{x}" for x in range(1, 11))
    not_required_fields.update(f"filter_value_{x}" for x in range(1, 11))
    not_required_fields.add("folder")


model_admins_to_register = [DownloadSettingsAdmin, LogInSettingsAdmin, ParsingSettingsAdmin, ReportAdmin]
helper_admin.register_models(model_admins_to_register)
