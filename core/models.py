from typing import Self

from parsing_helper import models as helper_models
from core.settings import Settings


class CoreModel(helper_models.BaseModel):
    class Meta:
        abstract = True

    settings = Settings()


class SingletonModel(CoreModel):
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
