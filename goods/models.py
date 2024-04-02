from django.contrib.auth.hashers import make_password, check_password
from email.policy import default
from enum import unique
from tabnanny import verbose
from unicodedata import category, digit
from unittest.util import _MAX_LENGTH
from django.db import models

from datetime import datetime

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return f'Категория - {self.name}'


class User(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=60, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=60, null=True, blank=True, verbose_name='Отчество')
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=12, null=True, blank=True, verbose_name='Телефон')
    password = models.CharField(default='',max_length=128, verbose_name='Пароль')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    rating = models.DecimalField(default=0.00, max_digits=5, decimal_places=2, verbose_name='Рейтинг')
    primary_payment_method = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE, related_name='primary_payment_method_for_user', null=True, blank=True, verbose_name='Основной способ оплаты')
    secondary_payment_method = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE, related_name='secondary_payment_method_for_user', null=True, blank=True, verbose_name='Дополнительный способ оплаты')    

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f'| Имя - {self.name} | Почта - {self.email} | Телефон - {self.phone} | Рейтинг - {self.rating} |'



class Product(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')
    manufacturer = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Производитель')
    date_added = models.DateField()

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
    
    def __str__(self) -> str:
        return f'| Название - {self.name} | Категория - {self.category} | Цена - {self.price} | Дата добавления - {self.date_added} |'


class Order(models.Model):
    client = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Клиент')
    order_date = models.DateField(verbose_name='Дата заказа')
    order_status = models.CharField(default='В обработке', max_length=50, verbose_name='Статус заказа')
    total_amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, verbose_name='Итоговая сумма') 
    

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        
    def __str__(self) -> str:
        return f'| Клиент - {self.client} | Дата добавления - {self.order_date} | Статус заказа - {self.order_status} |'


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.IntegerField(verbose_name='Количество')
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара на момент заказа')

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'
    
    def __str__(self) -> str:
        return f'| Клиент - {self.client} | Продукт - {self.product} | Количество - {self.quantity} | Итоговая стоимость - {self.price_at_order} |'


class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.IntegerField(default=0.00, verbose_name='Рейтинг')
    comment = models.TextField(verbose_name='Комментарий')
    date_added = models.DateField(verbose_name='Дата добавления')
    
    
    class Meta:
        db_table = 'review'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        
    def __str__(self) -> str:
        return f'| Продукт - {self.product} | Пользователь - {self.user} | Оценка - {self.rating} | Дата добавленя - {self.date_added} |'


class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Процент скидки')
    start_date = models.DateField(verbose_name='Дата начала действия скидки')
    end_date = models.DateField(verbose_name='Дата окончания действия скидки')
    final_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Итоговая цена', blank=True, null=True)

    class Meta:
        db_table = 'discount'
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self) -> str:
        return f'| Продукт - {self.product.name} | Цена - {self.product.price} | Скидка - {self.discount_percentage}% | Финальная цена - {self.final_price} | Начинается - {self.start_date} | Заканчивается - {self.end_date} |'

    def save(self, *args, **kwargs):
        if self.product and self.discount_percentage:
            current_date = datetime.now().date()
            if self.start_date <= current_date <= self.end_date:
                self.final_price = round(self.product.price - self.product.price * self.discount_percentage / 100, 2)
            else:
                self.final_price = None
        super().save(*args, **kwargs)


class PaymentMethod(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    name = models.CharField(max_length=50, verbose_name='Способ оплаты')

    class Meta:
        db_table = 'payment_method'
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'
    
    
    def __str__(self) -> str:
        return f'| Пользователь - {self.user} | Способ оплаты - {self.name} |'