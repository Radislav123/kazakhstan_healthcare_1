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
        verbose_name_plural = "download settings"


class LogInSettings(DamumedModel, core_models.LogInSettingsModel):
    class Meta:
        verbose_name_plural = "log in settings"

    login = models.CharField("Логин", max_length = 100)
    password = models.CharField("Пароль", max_length = 100)


class ParsingSettings(DamumedSingletonModel, core_models.ParsingSettingsModel):
    class Meta:
        verbose_name_plural = "parsing settings"


class Report(DamumedModel, core_models.ReportModel):
    pass


class ScreeningReport(DamumedModel, core_models.ReportModel):
    from_age = models.IntegerField("Фильтр возраста \"от\"", null = True)
    to_age = models.IntegerField("Фильтр возраста \"до\"", null = True)

    checkbox_title_1 = models.CharField("Галочка 1", max_length = 100, null = True)
    checkbox_title_2 = models.CharField("Галочка 2", max_length = 100, null = True)
    checkbox_title_3 = models.CharField("Галочка 3", max_length = 100, null = True)
    checkbox_title_4 = models.CharField("Галочка 4", max_length = 100, null = True)
    checkbox_title_5 = models.CharField("Галочка 5", max_length = 100, null = True)
    checkbox_title_6 = models.CharField("Галочка 6", max_length = 100, null = True)
    checkbox_title_7 = models.CharField("Галочка 7", max_length = 100, null = True)
    checkbox_title_8 = models.CharField("Галочка 8", max_length = 100, null = True)
    checkbox_title_9 = models.CharField("Галочка 9", max_length = 100, null = True)
    checkbox_title_10 = models.CharField("Галочка 10", max_length = 100, null = True)

    def get_checkbox_title(self, index: int) -> str | None:
        return getattr(self, f"checkbox_title_{index}")
