from imp import reload
# from .models import *
from django.apps import apps
from acorndx import settings
from django.contrib import admin
from django.urls import clear_url_caches
from django.utils.module_loading import import_module
from acorndxData.dataStructureInitial import abstract_model
# Register your models here.

# admin.site.register(Department)
# admin.site.register(UserInfo)
# admin.site.register(DataStructure)
abstract_model()
app_models = apps.get_app_config('acorndxData').get_models()
for model in app_models:
    # print(model)
    admin.site.register(model)
reload(import_module(settings.ROOT_URLCONF))
clear_url_caches()
