from django.contrib import admin
from ChecklistSeiscomp.models import ChecklistSeiscompModel, OperatorModel, StationListModel

# Register your models here.
class StationListAdmin(admin.ModelAdmin):
    list_display = ('kode', 'lokasi', 'tipe')
    search_fields = ('kode',)

admin.site.register(ChecklistSeiscompModel)
admin.site.register(OperatorModel)
admin.site.register(StationListModel, StationListAdmin)