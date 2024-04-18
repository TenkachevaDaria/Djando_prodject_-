from django.contrib import admin

# Register your models here.
from goods.models import Categories, Product, Subscriptions, Specification, Discount, Review

# admin.site.register(PaymentMethod)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', 'category',)}


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    prepopulated_fields = {}


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    prepopulated_fields = {}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    prepopulated_fields = {}