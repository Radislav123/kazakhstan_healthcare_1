from typing import Self

from django.db import models
from parsing_helper import models as helper_models

from core.settings import Settings
from core.validators import validate_path


class CoreModel(helper_models.BaseModel):
    class Meta:
        abstract = True

    settings = Settings()


class CoreSingletonModel(CoreModel):
    class Meta:
        abstract = True

    _object: Self = None

    def save(self, *args, **kwargs) -> None:
        obj = self.__class__.objects.all().first()
        if obj is not None:
            self.__class__.objects.all().exclude(id = self.id).delete()
        super().save(*args, **kwargs)

    @classmethod
    def get(cls) -> Self:
        if cls._object is None:
            cls._object = cls.objects.all().first()
        return cls._object


class DownloadSettingsModel(CoreSingletonModel):
    class Meta:
        abstract = True
        verbose_name_plural = "download settings"

    download = models.BooleanField("Скачивать")
    folder = models.CharField("Папка для скачивания", max_length = 1000, validators = [validate_path])
    format = models.CharField("Формат скачивания", max_length = 100)
    # в секундах
    max_download_waiting = models.IntegerField("Максимальное время ожидания скачивания")
    download_check_period = models.IntegerField("Период проверки скачивания")
    begin_date = models.DateField("Начало периода")
    end_date = models.DateField("Конец периода")


class LogInSettingsModel(CoreModel):
    class Meta:
        abstract = True
        verbose_name_plural = "log in settings"

    download = models.BooleanField("Скачивать")
    folder = models.CharField("Папка для скачивания", max_length = 1000, null = True)
    digital_signature_path = models.CharField("Путь ЭЦП", max_length = 1000, validators = [validate_path])
    digital_signature_password = models.CharField("Пароль ЭЦП", max_length = 100)
    logged_in = models.BooleanField("Последняя авторизация", null = True)
    downloaded = models.BooleanField("Последнее скачивание", null = True)
    download_duration = models.DurationField("Время скачивания всех отчетов", null = True)


class ParsingSettingsModel(CoreSingletonModel):
    class Meta:
        abstract = True
        verbose_name_plural = "parsing settings"

    show_browser = models.BooleanField("Показывать браузер", default = False)


class ReportModel(CoreModel):
    class Meta:
        abstract = True

    download = models.BooleanField("Скачивать")
    folder = models.CharField("Папка для скачивания", max_length = 1000, null = True)
    name = models.CharField("Название файла", max_length = 255)

    unique_together = ["folder", "name"]
