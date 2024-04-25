from django.contrib import admin

from basket.admin import BasketTabAdmin
from goods.admin import FavoriteProductAdmin
from users.models import User, PaymentMethod

# Register your models here.
class PaymentMethodAdminTab(admin.TabularInline):
    model = PaymentMethod
    fields = ["bank", "card_num"]
    readonly_fields = ["bank", "card_num"]
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions')
    list_display = ["username", "email", "phone"]
    search_fields = ["username", "email", "phone"]

    fields = [
        "username",
        ("first_name", "last_name", "middle_name", "image"),
        ("email", "phone"),
        "is_staff",
        "is_superuser",
        "is_active",
        ("groups", "user_permissions"),
        ("date_joined", "last_login"),
    ]
    # inlines = [FavoriteProductbAdmin]
    inlines = [PaymentMethodAdminTab, FavoriteProductAdmin, BasketTabAdmin]