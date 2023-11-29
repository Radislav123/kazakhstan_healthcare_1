from parsing_helper import admin as helper_admin

from core import models


class CoreAdmin(helper_admin.BaseAdmin):
    model = models.CoreModel


model_admins_to_register = []
helper_admin.register_models(model_admins_to_register)
