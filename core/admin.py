from parsing_helper import admin as helper_admin

from core import models


class CoreAdmin(helper_admin.BaseAdmin):
    model = models.CoreModel
