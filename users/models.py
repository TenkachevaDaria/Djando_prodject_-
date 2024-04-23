from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class PaymentMethod(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь', related_name='payment_methods')
    bank = models.CharField(default="Банк", max_length=50, verbose_name='Банк')
    card_num = models.CharField(max_length=50, verbose_name='Способ оплаты')
    date = models.CharField(default="00.00.00", max_length=8, verbose_name='Срок годности')
    CVV = models.CharField(default="000", max_length=3, verbose_name='CVV')

    class Meta:
        db_table = 'payment_method'
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'
    
    
    def __str__(self) -> str:
        return f'| Пользователь - {self.user} | Банк - {self.bank} | Способ оплаты - {self.card_num} |'


class User(AbstractUser):
    middle_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='Отчество')
    image = models.ImageField(upload_to='users_image', null=True, blank=True, verbose_name='Аватар')
    phone = models.CharField(max_length=12, null=True, blank=True, verbose_name='Телефон')
    rating = models.DecimalField(default=0.00, max_digits=5, decimal_places=2, verbose_name='Рейтинг')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Способ оплаты',  related_name='users')
      
    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self) -> str:
        return self.username

