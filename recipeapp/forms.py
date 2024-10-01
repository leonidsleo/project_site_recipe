from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Recipe, Categories

from django.core.exceptions import ValidationError


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'email': 'Эл. почта',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-input'}),
        }


    def clean_email(self):
        """
        Проверка уникальности эл. почты
        """


        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такая эл. почта существует')
        return email
    

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class RecipeAddForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), empty_label='Не выбрано', required=False, label='Категория')


    class Meta:
        model = Recipe
        fields = ['name', 'image', 'description', 'preparation_steps', 'preparation_time', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
            'preparation_steps': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }
        labels = {
            'name': 'Наименование(1)',
            'preparation_steps': 'Ингридиенты',
            'preparation_time': 'Время приготовления (мин)'
        }


class CategoryAddForm(forms.ModelForm):


    class Meta:
        model = Categories
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
        }        
        labels = {
            'name': 'Наименование категории'
        }


        def clean_name(self):
            name = self.cleaned_data['name']
            if User.objects.filter(name=name).exists():
                raise forms.ValidationError('Такая категория сществует')
            return name
        

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")