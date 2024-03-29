from django.contrib import admin

# Register your models here.
from goods.models import *

# admin.site.register(PaymentMethod)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', 'category',)}


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', 'last_name',)}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    prepopulated_fields = {}


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    prepopulated_fields = {}


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    prepopulated_fields = {}


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    prepopulated_fields = {}