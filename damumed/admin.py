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


class ScreeningAdmin(DamumedAdmin):
    model = models.Screening
    not_required_fields = {"folder", "from_age", "to_age"}
    not_required_fields.update(f"filter_title_{x}" for x in range(1, 11))
    not_required_fields.update(f"filter_value_{x}" for x in range(1, 11))
    not_required_fields.update(f"checkbox_title_{x}" for x in range(1, 11))
    extra_list_display = {
        "download": "filter_title_1",
        "folder": "filter_title_1",
        "name": "filter_title_1",
        "from_age": "filter_title_1",
        "to_age": "filter_title_1",
        **{f"checkbox_title_{x}": "filter_title_1" for x in range(1, 11)},
    }


class UnloadingAdmin(DamumedAdmin):
    model = models.Unloading
    not_required_fields = {"folder"}
    not_required_fields.update(f"filter_title_{x}" for x in range(1, 11))
    not_required_fields.update(f"filter_value_{x}" for x in range(1, 11))
    not_required_fields.update(f"step_{x}" for x in range(1, 11))
    extra_list_display = {
        "download": "filter_title_1",
        "folder": "filter_title_1",
        "name": "filter_title_1",
        **{f"step_{x}": "filter_title_1" for x in range(1, 11)},
    }


class ReportAdmin(DamumedAdmin):
    model = models.Report
    not_required_fields = {"folder", }
    not_required_fields.update(f"step_{x}" for x in range(1, 11))
    not_required_fields.update(f"filter_title_{x}" for x in range(1, 11))
    not_required_fields.update(f"filter_value_{x}" for x in range(1, 11))
    not_required_fields.update(f"checkbox_filter_title_{x}" for x in range(1, 11))
    not_required_fields.update(f"checkbox_filter_value_{x}" for x in range(1, 11))
    not_required_fields.update(f"multiple_filter_title_{x}" for x in range(1, 11))
    not_required_fields.update(f"multiple_filter_value_{x}" for x in range(1, 11))
    extra_list_display = {
        "download": "filter_title_1",
        "folder": "filter_title_1",
        "name": "filter_title_1",
        **{f"step_{x}": "filter_title_1" for x in range(1, 11)},
    }


model_admins_to_register = [
    DownloadSettingsAdmin,
    LogInSettingsAdmin,
    ParsingSettingsAdmin,
    ScreeningAdmin,
    UnloadingAdmin,
    ReportAdmin,
]
helper_admin.register_models(model_admins_to_register)
