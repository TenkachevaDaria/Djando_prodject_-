from django.db import models

from goods.models import Product
from users.models import User

# Create your models here.
class BasketQueryset(models.QuerySet):
    
    def total_price(self):
        return sum(basket.products_price() for basket in self)
    
    def total_quantity(self):
        if self:
            return sum(basket.quantity for basket in self)
        return 0


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Клиент')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Продукт')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    session_key = models.CharField(max_length=32, blank=True)
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    

    class Meta:
        db_table = 'basket'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
    
    objects = BasketQueryset().as_manager()
        
    def products_price(self):
        if self.product.discount_percentage:
            return round(round(self.product.price - self.product.price * self.product.discount_percentage / 100, 2) * self.quantity, 2)
        return round(self.product.price * self.quantity, 2)
