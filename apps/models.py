from django.db import models
from account.models import User
class Product(models.Model):
    class Meta:
        verbose_name = 'Техника'
        verbose_name_plural = 'техники'

    title = models.CharField('Название', max_length=50)
    image = models.ImageField("Изоброжание", upload_to='techniki/', blank=True, null=True)
    category = models.ForeignKey("Category", verbose_name=("Категории"), on_delete=models.CASCADE)
    price = models.DecimalField(("Цена"), max_digits=10, decimal_places=0, default=0)
    characteristic = models.ManyToManyField("Characteristics", verbose_name=("Характеристика"))
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    title = models.CharField(("Категории"), max_length=50)

    def __str__(self):
        return self.title
    

class Characteristics(models.Model):
    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    title = models.CharField(("Характеристика"), max_length=500)

    def __str__(self):
        return self.title