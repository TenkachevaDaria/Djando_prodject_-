from django.db import models

from users.models import User
from goods.models import Product

# Create your models here.
class OrderitemQueryset(models.QuerySet):
    
    def total_price(self):
        return sum(basket.products_price() for basket in self)
    
    def total_quantity(self):
        if self:
            return sum(basket.quantity for basket in self)
        return 0


class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name="Пользователь", default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания заказа")
    email = models.CharField(max_length=100, verbose_name="Почта")
    payment_method = models.CharField(default="Нет", max_length=100,verbose_name="Способ оплаты")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    status = models.CharField(max_length=50, default='В обработке', verbose_name="Статус заказа")

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(to=Product, on_delete=models.SET_DEFAULT, null=True, verbose_name="Продукт", default=None)
    name = models.CharField(max_length=150, verbose_name="Название")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата продажи")


    class Meta:
        db_table = "order_item"
        verbose_name = "Проданный товар"
        verbose_name_plural = "Проданные товары"

    objects = OrderitemQueryset.as_manager()

    def __str__(self):
        return f"Товар {self.name} | Заказ № {self.order.pk}"
    
    def products_price(self):
        if self.product.discount_percentage:
            return round(round(self.product.price - self.product.price * self.product.discount_percentage / 100, 2) * self.quantity, 2)
        return round(self.product.price * self.quantity, 2)