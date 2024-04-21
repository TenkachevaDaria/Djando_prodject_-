from django.contrib import admin

from basket.models import Basket

# Register your models here.
# admin.site.register(Basket)
class BasketTabAdmin(admin.TabularInline):
    model = Basket
    fields = "product", "quantity", "order_date"
    readonly_fields = ("order_date",)
    extra = 1


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ["user_display", "product", "quantity", "order_date"]
    list_filter = ["order_date", "user", "product"]
    search_fields = ["product"]

    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Анонимный пользователь"
