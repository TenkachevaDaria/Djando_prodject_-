from django.db import models

# Create your models here.
class Questions(models.Model):
    name = models.TextField(verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    
    
    class Meta:
        db_table = 'questions'
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        
    def __str__(self) -> str:
        return f'{self.name}'