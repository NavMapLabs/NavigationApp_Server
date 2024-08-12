from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.userPermission)
admin.site.register(models.map_data)
admin.site.register(models.map_editor)