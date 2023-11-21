from typing import Self

from django.db import models
from parsing_helper import models as helper_models

from eisz_downloader.validators import validate_path


class BaseModel(helper_models.BaseModel):
    class Meta:
        abstract = True


class SingletonModel(BaseModel):
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


class DownloadSettings(SingletonModel):
    class Meta:
        verbose_name_plural = "download settings"

    folder = models.CharField("Папка для скачивания", max_length = 1000, validators = [validate_path])
    format = models.CharField("Формат скачивания", max_length = 100)
    # в секундах
    max_download_waiting = models.IntegerField("Максимальное время ожидания скачивания")
    download_check_period = models.IntegerField("Период проверки скачивания")
    begin_date = models.DateField("Начало периода")
    end_date = models.DateField("Конец периода")


class LogInSettings(BaseModel):
    class Meta:
        verbose_name_plural = "log in settings"

    download = models.BooleanField("Скачивать")
    folder = models.CharField("Папка для скачивания", max_length = 1000, null = True)
    iin = models.IntegerField("ИИН")
    password = models.CharField("Пароль", max_length = 100)
    digital_signature_path = models.CharField("Путь ЭЦП", max_length = 1000, validators = [validate_path])
    digital_signature_password = models.CharField("Пароль ЭЦП", max_length = 100)
    logged_in = models.BooleanField("Последняя авторизация", null = True)
    downloaded = models.BooleanField("Последнее скачивание", null = True)
    download_duration = models.DurationField("Время скачивания всех отчетов", null = True)


class ParsingSettings(SingletonModel):
    class Meta:
        verbose_name_plural = "parsing settings"

    show_browser = models.BooleanField("Показывать браузер", default = False)


class Report(BaseModel):
    download = models.BooleanField("Скачивать")
    folder = models.CharField("Папка для скачивания", max_length = 1000, null = True)
    name = models.CharField("Название файла", max_length = 255)

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
