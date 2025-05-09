from django.contrib import admin
from .models import QcRecord, ErrorStation

# Register your models here.
admin.site.register(QcRecord)
admin.site.register(ErrorStation)