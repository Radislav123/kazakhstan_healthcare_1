from django.db import models

from core import models as core_models
from damumed.settings import Settings


class DamumedModel(core_models.CoreModel):
    class Meta:
        abstract = True

    settings = Settings()


class DamumedSingletonModel(DamumedModel, core_models.CoreSingletonModel):
    class Meta:
        abstract = True


class DownloadSettings(DamumedSingletonModel, core_models.DownloadSettingsModel):
    class Meta:
        verbose_name_plural = "настройки скачивания"


class LogInSettings(DamumedModel, core_models.LogInSettingsModel):
    class Meta:
        verbose_name_plural = "настройки аутентификации"

    domain = models.CharField("Домен", max_length = 100)
    login = models.CharField("Логин", max_length = 100)
    password = models.CharField("Пароль", max_length = 100)


class ParsingSettings(DamumedSingletonModel, core_models.ParsingSettingsModel):
    class Meta:
        verbose_name_plural = "настройки парсинга"


class Screening(DamumedModel, core_models.CheckboxMixin, core_models.FiltersMixin, core_models.ReportModel):
    class Meta:
        verbose_name_plural = "скрининги"

    from_age = models.IntegerField("Фильтр возраста \"от\"", null = True)
    to_age = models.IntegerField("Фильтр возраста \"до\"", null = True)


class Unloading(DamumedModel, core_models.StepsMixin, core_models.FiltersMixin, core_models.ReportModel):
    class Meta:
        verbose_name_plural = "выгрузки"


class Report(
    DamumedModel,
    core_models.CheckboxFiltersMixin,
    core_models.MultipleFiltersMixin,
    core_models.StepsMixin,
    core_models.FiltersMixin,
    core_models.ReportModel
):
    class Meta:
        verbose_name_plural = "отчеты"
