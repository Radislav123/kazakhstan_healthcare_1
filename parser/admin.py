from django.contrib import admin
from parsing_helper import admin as helper_admin


class BaseAdmin(helper_admin.BaseAdmin):
    pass


model_admins_to_register = []
helper_admin.register_models(model_admins_to_register)
