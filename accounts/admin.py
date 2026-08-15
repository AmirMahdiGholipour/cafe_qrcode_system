from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CafeModel, CafeStaffModel, CafeMembership
from django.utils.html import format_html


@admin.register(CafeModel)
class CafeModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_preview']
    search_fields = ['name']
    readonly_fields = ['logo_preview']

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="100" height="100" />', obj.logo.url)
        return "No logo available"

class CafeMembershipInline(admin.TabularInline):
    model = CafeMembership
    extra = 0
    autocomplete_fields = ['cafe']


@admin.register(CafeStaffModel)
class CafeStaffAdmin(UserAdmin):
    list_display = ["username", "first_name", "last_name", "phone_number", "is_active"]
    list_filter = ["is_active", "gender"]
    search_fields = ["username", "first_name", "last_name", "phone_number", "national_code"]
    inlines = [CafeMembershipInline]

    fieldsets = UserAdmin.fieldsets + (
        ("اطلاعات تکمیلی", {
            "fields": ("phone_number", "national_code", "address", "province", "city", "gender"),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("اطلاعات تکمیلی", {
            "fields": ("phone_number", "national_code", "address", "province", "city", "gender"),
        }),
    )


@admin.register(CafeMembership)
class CafeMembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "cafe", "role", "created_at"]
    list_filter = ["role", "cafe"]
    search_fields = ["user__username", "cafe__name"]
    list_select_related = ["user", "cafe"]
    autocomplete_fields = ["user", "cafe"]