from django.contrib import admin

from basket.admin import BasketTabAdmin
from users.models import User, PaymentMethod

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions')
    list_display = ["username", "email", "phone", "rating"]
    search_fields = ["username", "email", "phone"]

    fields = [
        ("username", "rating"),
        ("first_name", "last_name", "middle_name", "image"),
        ("email", "phone"),
        ("primary_payment_method", "secondary_payment_method"),
        "is_staff",
        "is_superuser",
        "is_active",
        ("groups", "user_permissions"),
        ("date_joined", "last_login"),
    ]

    inlines = [BasketTabAdmin]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ["user", "name"]
    search_fields = ["user"]