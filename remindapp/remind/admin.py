from django.contrib import admin
from .models import RemindModel, CustomUsers
from django.contrib.auth.admin import UserAdmin

class CustomUsersAdmin(UserAdmin):
    model = CustomUsers
    list_display = ("mailaddress", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("mailaddress", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("mailaddress", "password1", "password2", "is_staff", "is_active")}
        ),
    )
    ordering = ("mailaddress",)

admin.site.register(CustomUsers, CustomUsersAdmin)
# Register your models here.
admin.site.register(RemindModel)