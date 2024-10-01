from django.urls import path

from . import views
from project_site_recipe import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('recipe/', views.recipe_a, name='recipe'),
    path('recipeadd/', views.recipeadd, name='recipeadd'),
    path('recipe_edit/<int:id>', views.recipe_edit, name='recipeedit'),
    path('recipeshow/<int:recipe_id>', views.recipeshow,name='recipeshow'),
    path('registracion/', views.RegisterUser.as_view(), name='registracion'),
    path('login/', views.LoginUser.as_view(), name='login'),  
    path('logout/', views.logout_user, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('category/', views.categoryadd, name='category') 
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)