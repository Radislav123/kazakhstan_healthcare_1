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


class ParsingSettings(DamumedSingletonModel, core_models.ParsingSettingsModel):
    class Meta:
        verbose_name_plural = "parsing settings"


class Report(DamumedModel, core_models.ReportModel):
    pass
