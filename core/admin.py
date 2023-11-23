from parsing_helper import admin as helper_admin

from core import models


class CoreAdmin(helper_admin.BaseAdmin):
    model = models.CoreModel


class CoreSettingsAdmin(CoreAdmin):
    model = models.CoreSettings


model_admins_to_register = [CoreSettingsAdmin]
helper_admin.register_models(model_admins_to_register)
