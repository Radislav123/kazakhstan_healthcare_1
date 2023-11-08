from django.db import models
from parsing_helper import models as helper_models
from parser.validators import validate_path


class BaseModel(helper_models.BaseModel):
    class Meta:
        abstract = True


class SingletonModel(BaseModel):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        obj = self.__class__.objects.all().first()
        if obj is not None:
            self.__class__.objects.all().exclude(id = self.id).delete()
        super().save(*args, **kwargs)


class DownloadSettings(SingletonModel):
    class Meta:
        verbose_name_plural = "download settings"

    download_folder = models.CharField("Папка для скачивания", max_length = 1000, validators = [validate_path])
