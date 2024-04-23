from django.contrib import admin
from django.forms import DateInput
from django.db import models
# Register your models here.
from goods.models import (
    Categories,
    Product,
    Subscriptions,
    Review,
)

# admin.site.register(PaymentMethod)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "subscription", "manufacturer", "price", "discount_percentage", "average_rating"]
    search_fields = ["name", "manufacturer"]
    prepopulated_fields = {"slug": ("name", "category")}
    list_filter = ["category", "subscription", "manufacturer"]
    list_editable = ["discount_percentage"]
    fields = [
        ("name", "manufacturer", "average_rating"),
        "slug",
        "description",
        "peculiarities",
        ("category", "subscription", "image"),
        "price",
    ]


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["product", "user", "rating", "date_added", "comment"]
    search_fields = ["product", "user", "comment"]
    list_filter = ["rating", "user", "product"]