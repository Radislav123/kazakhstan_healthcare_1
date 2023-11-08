from parsing_helper import admin as helper_admin

from parser import models


class BaseAdmin(helper_admin.BaseAdmin):
    model = models.BaseModel


class DownloadSettingsAdmin(BaseAdmin):
    model = models.DownloadSettings


model_admins_to_register = [DownloadSettingsAdmin]
helper_admin.register_models(model_admins_to_register)
