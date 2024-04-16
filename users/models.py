from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    middle_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='Отчество')
    image = models.ImageField(upload_to='users_image', null=True, blank=True, verbose_name='Аватар')
    phone = models.CharField(max_length=12, null=True, blank=True, verbose_name='Телефон')
    rating = models.DecimalField(default=0.00, max_digits=5, decimal_places=2, verbose_name='Рейтинг')
    primary_payment_method = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE, related_name='primary_payment_method_for_user', null=True, blank=True, verbose_name='Основной способ оплаты')
    secondary_payment_method = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE, related_name='secondary_payment_method_for_user', null=True, blank=True, verbose_name='Дополнительный способ оплаты') 
    
    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self) -> str:
        return self.username


class PaymentMethod(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    name = models.CharField(max_length=50, verbose_name='Способ оплаты')

    class Meta:
        db_table = 'payment_method'
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'
    
    
    def __str__(self) -> str:
        return f'| Пользователь - {self.user} | Способ оплаты - {self.name} |'
