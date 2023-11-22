from django.db import models

from core import models as core_models
from eisz.settings import Settings


class EISZModel(core_models.CoreModel):
    class Meta:
        abstract = True

    settings = Settings()


class EISZSingletonModel(EISZModel, core_models.CoreSingletonModel):
    class Meta:
        abstract = True


class DownloadSettings(EISZSingletonModel, core_models.DownloadSettingsModel):
    class Meta:
        verbose_name_plural = "download settings"


class LogInSettings(EISZModel, core_models.LogInSettingsModel):
    class Meta:
        verbose_name_plural = "log in settings"

    iin = models.IntegerField("ИИН")
    password = models.CharField("Пароль", max_length = 100)


class ParsingSettings(EISZSingletonModel, core_models.ParsingSettingsModel):
    class Meta:
        verbose_name_plural = "parsing settings"


class Report(EISZModel, core_models.ReportModel):
    step_1 = models.CharField("Шаг 1", max_length = 1000, null = True)
    step_2 = models.CharField("Шаг 2", max_length = 1000, null = True)
    step_3 = models.CharField("Шаг 3", max_length = 1000, null = True)
    step_4 = models.CharField("Шаг 4", max_length = 1000, null = True)
    step_5 = models.CharField("Шаг 5", max_length = 1000, null = True)
    step_6 = models.CharField("Шаг 6", max_length = 1000, null = True)
    step_7 = models.CharField("Шаг 7", max_length = 1000, null = True)

    filter_title_1 = models.CharField("Название фильтра 1", max_length = 100, null = True)
    filter_value_1 = models.CharField("Значение фильтра 1", max_length = 100, null = True)
    filter_title_2 = models.CharField("Название фильтра 2", max_length = 100, null = True)
    filter_value_2 = models.CharField("Значение фильтра 2", max_length = 100, null = True)
    filter_title_3 = models.CharField("Название фильтра 3", max_length = 100, null = True)
    filter_value_3 = models.CharField("Значение фильтра 3", max_length = 100, null = True)
    filter_title_4 = models.CharField("Название фильтра 4", max_length = 100, null = True)
    filter_value_4 = models.CharField("Значение фильтра 4", max_length = 100, null = True)
    filter_title_5 = models.CharField("Название фильтра 5", max_length = 100, null = True)
    filter_value_5 = models.CharField("Значение фильтра 5", max_length = 100, null = True)
    filter_title_6 = models.CharField("Название фильтра 6", max_length = 100, null = True)
    filter_value_6 = models.CharField("Значение фильтра 6", max_length = 100, null = True)
    filter_title_7 = models.CharField("Название фильтра 7", max_length = 100, null = True)
    filter_value_7 = models.CharField("Значение фильтра 7", max_length = 100, null = True)
    filter_title_8 = models.CharField("Название фильтра 8", max_length = 100, null = True)
    filter_value_8 = models.CharField("Значение фильтра 8", max_length = 100, null = True)
    filter_title_9 = models.CharField("Название фильтра 9", max_length = 100, null = True)
    filter_value_9 = models.CharField("Значение фильтра 9", max_length = 100, null = True)
    filter_title_10 = models.CharField("Название фильтра 10", max_length = 100, null = True)
    filter_value_10 = models.CharField("Значение фильтра 10", max_length = 100, null = True)

    def get_step_path(self, step: int) -> str | None:
        return getattr(self, f"step_{step}")

    def get_filter_title(self, index: int) -> str | None:
        return getattr(self, f"filter_title_{index}")

    def get_filter_value(self, index: int) -> str | None:
        return getattr(self, f"filter_value_{index}")
