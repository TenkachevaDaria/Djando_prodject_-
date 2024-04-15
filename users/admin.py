from django.contrib import admin

from users.models import User, PaymentMethod

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    prepopulated_fields = {}


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    prepopulated_fields = {}