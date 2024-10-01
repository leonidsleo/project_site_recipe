from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse


class Categories(models.Model):
    """
    Класс добавления категорий
    """


    name = models.CharField(max_length=70, null=True)


    def __str__(self) :
        return self.name
    

class Recipe(models.Model):
    """
    Класс добавление рецепта
    """

    
    name = models.CharField(max_length=70, blank=False, verbose_name='Имя рецепта:')
    description = models.CharField(max_length=2000, blank=False, verbose_name='Как готовить:')
    preparation_steps = models.TextField(blank=False, verbose_name='Из чего готовим:')
    preparation_time = models.IntegerField(blank=True, verbose_name='Сколько мин.:')
    autor = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='folk_recipe', verbose_name='Автор')
    category = models.ForeignKey(Categories, on_delete=models.SET_DEFAULT, default='no_category', related_name="нет", verbose_name='Категория:', blank=True)
    data = models.DateField(auto_now_add=True, verbose_name='Дата добавления:') 
    image = models.ImageField(verbose_name='Фото:', blank=True, upload_to='img/', default=None, null=True)


    def __str__(self):
        return f'Добавлен рецепт {self.name}'
    

    def get_absolute_url(self):
        """
        Функция формиования абсолютной ссылки на объект (url адрес)
        """


        return reverse('recipeshow', kwargs={'recipe_id': self.pk})