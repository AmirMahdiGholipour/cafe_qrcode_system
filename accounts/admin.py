from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CafeModel, CafeStaffModel
from django.utils.html import format_html


@admin.register(CafeModel)
class CafeModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_preview']
    readonly_fields = ['logo_preview']

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="100" height="100" />', obj.logo.url)
        return "No logo available"


@admin.register(CafeStaffModel)
class CafeStaffModelAdmin(UserAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'role', 'cafe']
    list_filter = ['role', 'cafe']
    search_fields = ['username', 'first_name', 'last_name', 'cafe__name', 'role']
    list_select_related = ["cafe"]

    fieldsets = UserAdmin.fieldsets + (
    ('Cafe Information', {'fields': ('cafe', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
    ('Cafe Information', {'fields': ('cafe', 'role')}),
    )