from django.contrib import admin
from .models import * #アナザー追記defaultgoods, mygoods
from django.contrib.auth.admin import UserAdmin

class CustomUsersAdmin(UserAdmin):
    model = CustomUsers
    list_display = ("uuid", "mailaddress", "default_term", "is_staff", "is_active")
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

class MyGoodsAdmin(admin.ModelAdmin):
    list_display = ("id", "uid", "goods_name", "category", "purchase_date", "next_purchase_date", "expire_date", "next_purchase_term", "first_term")

# MANA追記　サイト管理画面に表示
admin.site.register(CustomUsers, CustomUsersAdmin)
# Register your models here.
admin.site.register(RemindModel)
admin.site.register(DefaultGoods) #アナザー追記defaultgoods, mygoods
admin.site.register(MyGoods, MyGoodsAdmin) #アナザー追記defaultgoods, mygoods
