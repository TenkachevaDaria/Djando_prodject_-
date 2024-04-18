from django.db import models

from goods.models import Discount, Product
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
        return round(self.product.price * self.quantity, 2)

    def __str__(self) -> str:
        return f'| Клиент - {self.user.username}| Товар - {self.product.name} | Дата добавления - {self.order_date} | Количество товара - {self.quantity} |'