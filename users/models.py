from django.contrib.auth.hashers import make_password, check_password
from django.db import models

# Create your models here.
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


class PaymentMethod(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    name = models.CharField(max_length=50, verbose_name='Способ оплаты')

    class Meta:
        db_table = 'payment_method'
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'
    
    
    def __str__(self) -> str:
        return f'| Пользователь - {self.user} | Способ оплаты - {self.name} |'
