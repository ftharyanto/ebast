from django.contrib import admin
from .models import QcRecord, Operator

# Register your models here.
admin.site.register(QcRecord)
admin.site.register(Operator)