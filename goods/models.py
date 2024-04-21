from enum import unique
from django.db import models
from datetime import datetime

from django.urls import reverse
from users.models import User

# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return f'{self.name}'


class Subscriptions(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Срок подписки')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'subscription'
        verbose_name = 'Периоды подписок'
        verbose_name_plural = 'Период подписки'

    def __str__(self) -> str:
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    peculiarities = models.TextField(blank=True, null=True, verbose_name='Особенности')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')
    manufacturer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Производитель')
    date_added = models.DateField(verbose_name='Дата добавления')
    subscription = models.ForeignKey(to=Subscriptions, on_delete=models.CASCADE, verbose_name='Период подписки', blank=True, null=True)

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('id',)
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})
    


class Features(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features', verbose_name='Продукт')
    description = models.TextField(null=True, blank=True, verbose_name='Описание особенностей')

    def __str__(self) -> str:
        return f'{self.product.name}'


class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='licenses', verbose_name='Товар')
    media_type = models.CharField(max_length=100, null=True, blank=True, verbose_name='Тип носителя')
    delivery_type = models.CharField(max_length=100, null=True, blank=True, verbose_name='Тип поставки')
    purpose = models.CharField(max_length=100, null=True, blank=True, verbose_name='Назначение')
    validity_period = models.CharField(max_length=100, null=True, blank=True, verbose_name='Срок действия')
    bitness = models.CharField(max_length=20, null=True, blank=True, verbose_name='Разрядность')

    
    class Meta:
        db_table = 'specification'
        verbose_name = 'Спецификации'
        verbose_name_plural = 'Спецификация'

    def __str__(self):
        return f'{self.product.name}'


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

    

class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.FloatField(default=0.00, verbose_name='Рейтинг')
    comment = models.TextField(verbose_name='Комментарий')
    date_added = models.DateField(verbose_name='Дата добавления')
    
    
    class Meta:
        db_table = 'review'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        
    def __str__(self) -> str:
        return f'| Продукт - {self.product.name} | Пользователь - {self.user.username} | Оценка - {self.rating} | Дата добавленя - {self.date_added} |'

    def star_rating(self):
        rating_int = int(self.rating)
        rating_float = self.rating - rating_int
        anti_rating = int(5 - self.rating)
        return rating_int, rating_float, anti_rating