from django.contrib import admin

# Register your models here.
from goods.models import (
    Categories,
    Product,
    Subscriptions,
    Specification,
    Discount,
    Review,
)

# admin.site.register(PaymentMethod)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "subscription", "manufacturer", "price", "average_rating"]
    search_fields = ["name"]
    list_filter = ["category", "subscription", "manufacturer"]
    fields = [
        ("name", "manufacturer", "average_rating"),
        "slug",
        "description",
        "peculiarities",
        ("category", "subscription", "image"),
        "price",
        "date_added"
    ]


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ["product", "media_type", "delivery_type", "purpose", "validity_period", "bitness"]
    search_fields = ["product"]
    list_editable = ["media_type", "delivery_type", "purpose", "validity_period", "bitness"]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ["product", "discount_percentage", "final_price", "start_date", "end_date"]
    search_fields = ["product"]
    list_editable = ["discount_percentage", "start_date", "end_date"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["product", "user", "rating", "date_added", "comment"]
    search_fields = ["product", "user", "comment"]
    list_filter = ["rating", "user", "product"]