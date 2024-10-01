from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from .forms import LoginUserForm, RegisterUserForm, RecipeAddForm
from .forms import CategoryAddForm
from .models import User, Recipe
from random import choice
from django.contrib.auth import logout 
from django.contrib.auth.views import LoginView 
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView 
import logging


logger = logging.getLogger(__name__)


def index(request): 
    """
    Главная страница с показом 5 рандомных рецептов.
    Рецепты показываются как ссылки.
    И показываются в виде блоков
    """


    recipe_five = Recipe.objects.all()
    recipe_list = []
    if len(recipe_five) > 5:
        while len(recipe_list) < 5:
            r = choice(recipe_five)
            if r not in recipe_list:
                recipe_list.append(r)
    else:
        recipe_list = recipe_five
    

    data = {
        'recipe_five': recipe_list,
        'title': 'Главная'
    }
    logger.info('Start page index')
    return render(request, 'recipeapp/index.html', data)


def recipe_a(request):
    """
    Вывод всех рецептов на странице
    """
    
    
    recipe_all = Recipe.objects.all()
    return render(request, 'recipeapp/recipe.html', {'recipe_all': recipe_all, 'title': 'Все рецепты'})


def recipeshow(request, recipe_id):
    """
    Показать полностью один рецепт
    """


    recipe_show = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipeapp/recipe_show.html', {'recipe_show': recipe_show})


@login_required(login_url='/login/')
def recipeadd(request):
    """
    Добавить рецепт.
    Функция защищена декоратором, который запрещает доступ
    к функции не зарегестрированных пользователей.  
    """


    if request.method == 'POST':
        form = RecipeAddForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            preparation_steps = form.cleaned_data['preparation_steps']
            preparation_time = form.cleaned_data['preparation_time']
            autor = User.objects.get(pk=request.user.id)
            category = form.cleaned_data['category']
            image = form.cleaned_data['image']
            recipe = Recipe(name=name,
                            description=description,
                            preparation_steps=preparation_steps,
                            preparation_time=preparation_time,
                            autor=autor,
                            category=category,
                            image=image)
            recipe.save()
            return redirect('index')
    else:
        form = RecipeAddForm()

    slovar = {
        'title': 'Добавить рецепт',
        'form':form
    }
    logger.info(f'Add recipe')
    return render(request, 'recipeapp/recipeadd.html', slovar)


@login_required(login_url='/login/')
def recipe_edit(request, id:int):
    """
    Изменение рецепта.
    Функция защищена декоратором, который запрещает доступ
    к функции не зарегестрированных пользователей.      
    """
    recipe_ed = get_object_or_404(Recipe, pk=id)
    if request.user.id == recipe_ed.autor.id:
        if request.method == 'POST':
            form = RecipeAddForm(request.POST, request.FILES)
            if form.is_valid():
                recipe_ed.name = form.cleaned_data['name']
                recipe_ed.description = form.cleaned_data['description']
                recipe_ed.preparation_steps = form.cleaned_data['preparation_steps']
                recipe_ed.preparation_time = form.cleaned_data['preparation_time']
                recipe_ed.category = form.cleaned_data['category']
                recipe_ed.image = form.cleaned_data['image']
                recipe_ed.save()
                return redirect('index')
        else:
            form = RecipeAddForm(instance=recipe_ed)
        slovar = {
            'title': 'Изменить рецепт',
            'form':form
        }
        return render(request, 'recipeapp/recipe_edit.html', slovar)
    else:
        return HttpResponse("Редактировать может только автор")
    

@login_required(login_url='/login/')
def categoryadd(request):
    """
    Добавление категории.
    Функция защищена декоратором, который запрещает доступ
    к функции не зарегестрированных пользователей. 
    """


    if request.method == 'POST':
        form = CategoryAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CategoryAddForm()
    dannie = {
        'title': 'Добавить категорию',
        'form': form
    }
    return render(request, 'recipeapp/categoryadd.html', dannie)


class RegisterUser(CreateView):
    """
    Регистрация пользователей
    """
    form_class = RegisterUserForm
    template_name = 'recipeapp/registracion.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('login')



class LoginUser(LoginView):
    """
    Вход зарегистрированных пользователей
    """

    form_class = LoginUserForm 
    template_name = 'recipeapp/login.html'
    extra_context = {'title': 'Авторизация'}

    logger.info(f'User is logged in system')


    def get_success_url(self): 
        """
        ф-я куда перенаправить пользователя после авторизации
        """

        return reverse_lazy('recipe')


def logout_user(request):
    """
    Выход пользоватея
    """


    logout(request)
    return HttpResponseRedirect(reverse('index'))


def contact(request):
    return render(request, 'recipeapp/contact.html')