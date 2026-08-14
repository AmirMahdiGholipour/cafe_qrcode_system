from django.contrib import admin
from .models import CafeModel
from django.utils.html import format_html


@admin.register(CafeModel)
class CafeModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_preview']
    readonly_fields = ['logo_preview']

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="100" height="100" />', obj.logo.url)
        return "No logo available"