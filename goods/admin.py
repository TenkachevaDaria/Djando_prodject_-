from django.contrib import admin
# Register your models here.
from goods.models import (
    Categories,
    FavoriteProduct,
    Product,
    Subscriptions,
    Review,
)

# admin.site.register(PaymentMethod)
class FavoriteProductAdmin(admin.TabularInline):
    model = FavoriteProduct
    readonly_fields = ["product"]
    extra = 1


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "in_stock", "category", "subscription", "manufacturer", "price", "discount_percentage", "average_rating"]
    search_fields = ["name", "manufacturer"]
    prepopulated_fields = {"slug": ("name", "category")}
    list_filter = ["category", "in_stock", "subscription", "manufacturer"]
    list_editable = ["in_stock", "discount_percentage"]
    fields = [
        ("name", "manufacturer", "average_rating"),
        ("slug", "in_stock"),
        "description",
        "peculiarities",
        ("category", "subscription", "image"),
        ('media_type', 'delivery_type', 'purpose', 'bitness'),
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