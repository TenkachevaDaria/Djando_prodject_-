from enum import unique
from django.db import models
from django.db.models import Avg
from django.urls import reverse
from users.models import User
from django.utils.text import slugify

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
    discount_percentage = models.DecimalField(default=0.00, max_digits=5, decimal_places=2, verbose_name='Процент скидки')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')
    manufacturer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Производитель')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    subscription = models.ForeignKey(to=Subscriptions, on_delete=models.CASCADE, verbose_name='Период подписки', blank=True, null=True)
    average_rating = models.FloatField(default=0.00, verbose_name='Средний рейтинг')
    in_stock = models.CharField(default="Да", max_length=3, null=True, blank=True, verbose_name='Наличие товара')
    media_type = models.CharField(max_length=100, null=True, blank=True, verbose_name='Тип носителя')
    delivery_type = models.CharField(max_length=100, null=True, blank=True, verbose_name='Тип поставки')
    purpose = models.CharField(max_length=100, null=True, blank=True, verbose_name='Назначение')
    bitness = models.CharField(max_length=20, null=True, blank=True, verbose_name='Разрядность')

    class Meta:
        db_table = 'product'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('id',)
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})
    
    def save(self, *args, **kwargs):
        # Если slug пустой, генерируем его на основе имени товара и имени производителя
        if not self.slug:
            self.slug = slugify(f"{self.name} {self.category.id}")
        super().save(*args, **kwargs)
    
    def update_average_rating(self):
        average_rating = self.review_set.aggregate(avg_rating=Avg('rating'))['avg_rating']
        if average_rating is not None:
            self.average_rating = round(average_rating, 2)
        else:
            self.average_rating = 0.00
        self.save()

    def discount_price(self):
        return round(self.price - self.price * self.discount_percentage / 100, 2)
        

class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Избранный продукт')

    class Meta:
        verbose_name = 'Избранный продукт'
        verbose_name_plural = 'Избранные продукты'
    
    def __str__(self) -> str:
        return f'{self.product.name}'


class Features(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features', verbose_name='Продукт')
    description = models.TextField(null=True, blank=True, verbose_name='Описание особенностей')

    def __str__(self) -> str:
        return f'{self.product.name}'


class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.FloatField(default=0.00, verbose_name='Рейтинг')
    comment = models.TextField(verbose_name='Комментарий')
    date_added = models.DateField(auto_now_add=True, verbose_name='Дата добавления')
    
    
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
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_average_rating()