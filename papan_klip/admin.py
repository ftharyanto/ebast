from django.contrib import admin
from .models import PapanKlip

@admin.register(PapanKlip)
class PapanKlipAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'expires_at')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
