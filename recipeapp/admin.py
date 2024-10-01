from django.contrib import admin

from django.db.models.query import QuerySet
from django.http import HttpRequest

from .models import Recipe, Categories


@admin.action(description='Пометить удаленным')
def my_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    """пометить на удаление (заархивировать) вместо удаления"""

    queryset.update(archived=True)


@admin.action(description='Снять пометку на удаление')
def my_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    """снять пометку на удаление"""

    queryset.update(archived=False)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    """ отображение КатегориЙ в админ панеле:
        отображаемые поля 
        поля ссылок для перехода в объект
    """
    
    list_display = 'pk', 'name'
    list_display_links = 'pk', 


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """ отображение таблицы рецептов в админке:
        отображаемые поля
        сортировка
        групповые действия
        поля ссылок для перехода в объект
        поиск по ...
        настраиваем карточку объекта
    """

    list_display = 'pk', 'name', 'category'
    ordering = 'pk',
    actions = [
        my_archived,
        my_unarchived,
    ] 
    list_display_links = 'pk', 'name'
    search_fields = 'name', 'description', 'category'
    fieldsets = [
        (None, {           
            'fields': ('name', 'description'),
        }),
        ('Принадлежность', {            
            'fields': ('autor', 'category'),            
            'classes': ('collapse', 'wide'),            
            'description': "Здесь пиши, что хочешь"
        }),
        ('Из чего приготовим и за сколько', {
            'fields': ('preparation_steps', 'preparation_time'),
        })
    ]  