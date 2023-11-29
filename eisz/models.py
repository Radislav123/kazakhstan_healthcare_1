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
        verbose_name_plural = "настройки скачивания"

    format = models.CharField("Формат скачивания", max_length = 100)


class LogInSettings(EISZModel, core_models.LogInSettingsModel):
    class Meta:
        verbose_name_plural = "настройки аутентификации"

    iin = models.IntegerField("ИИН")
    password = models.CharField("Пароль", max_length = 100)
    digital_signature_path = models.CharField("Путь ЭЦП", max_length = 1000, validators = [validate_path])
    digital_signature_password = models.CharField("Пароль ЭЦП", max_length = 100)


class ParsingSettings(EISZSingletonModel, core_models.ParsingSettingsModel):
    class Meta:
        verbose_name_plural = "настройки парсинга"


class Report(EISZModel, core_models.StepsMixin, core_models.FiltersMixin, core_models.ReportModel):
    class Meta:
        verbose_name_plural = "отчеты"
