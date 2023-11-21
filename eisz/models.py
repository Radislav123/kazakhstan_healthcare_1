from core import models as core_models
from eisz.settings import Settings


class EISZModel(core_models.CoreModel):
    class Meta:
        abstract = True

    settings = Settings()


class EISZSingletonModel(core_models.CoreSingletonModel, EISZModel):
    class Meta:
        abstract = True


class DownloadSettings(EISZSingletonModel, core_models.DownloadSettingsModel):
    pass


class LogInSettings(EISZModel, core_models.LogInSettingsModel):
    pass


class ParsingSettings(EISZSingletonModel, core_models.ParsingSettingsModel):
    pass


class Report(EISZModel, core_models.ReportModel):
    pass
