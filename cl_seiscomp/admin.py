from django.contrib import admin
from .models import StationListModel, CsRecordModel

# Register your models here.
admin.site.register(StationListModel)
admin.site.register(CsRecordModel)