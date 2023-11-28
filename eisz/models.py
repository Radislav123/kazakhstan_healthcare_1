from django.db import models

from core import models as core_models
from core.validators import validate_path
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
    digital_signature_path = models.CharField("Путь ЭЦП", max_length = 1000, validators = [validate_path])
    digital_signature_password = models.CharField("Пароль ЭЦП", max_length = 100)


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
    step_8 = models.CharField("Шаг 8", max_length = 1000, null = True)
    step_9 = models.CharField("Шаг 9", max_length = 1000, null = True)
    step_10 = models.CharField("Шаг 10", max_length = 1000, null = True)

    def get_step_path(self, step: int) -> str | None:
        return getattr(self, f"step_{step}")
