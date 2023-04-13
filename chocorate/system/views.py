from sqladmin import ModelView
from .models import System


class SystemAdmin(ModelView, model=System):
    column_list = list(System.__fields__)
