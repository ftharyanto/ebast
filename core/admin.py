from django.contrib import admin
from .models import Operator, Kelompok

class OperatorProperty(admin.ModelAdmin):
  list_display = ("name", "NIP")

# Register your models here.
admin.site.register(Operator, OperatorProperty)
admin.site.register(Kelompok)