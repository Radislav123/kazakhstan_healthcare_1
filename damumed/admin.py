from django.contrib import messages
from django.core.management import call_command
from django.db import models as django_models
from django.http import HttpRequest
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
    actions = ("download_not_finished",)

    def download_not_finished(self, request: HttpRequest, queryset: django_models.QuerySet) -> None:
        self.message_user(request, "Начато повторное скачивание", messages.SUCCESS)

        not_requested = models.LogInSettings.objects.filter(download = True).exclude(id__in = [x.id for x in queryset])
        not_requested_ids = [x.id for x in not_requested]
        models.LogInSettings.objects.filter(id__in = not_requested_ids).update(download = False)

        log_in_ids = [x.id for x in queryset.filter(downloaded = True, download = True)]
        queryset.filter(id__in = log_in_ids).update(download = False)
        call_command("damumed_log_in")
        call_command("damumed_download")
        queryset.filter(id__in = log_in_ids).update(download = True)

        models.LogInSettings.objects.filter(id__in = not_requested_ids).update(download = True)


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
