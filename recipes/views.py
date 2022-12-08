from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.recipes.factory import make_recipe
from recipes.models import Recipe 

def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={'recipes': recipes})

def category(request, category_id):
    #recipes = Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id') # category_id é igual ao category_id da recipes
    recipes = get_list_or_404(Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id'))

    return render(request, 'recipes/pages/category.html', context={'recipes': recipes, 'title': recipes[0].category.name})

def recipe(request, id):
    #recipe = Recipe.objects.filter(id=id)
    recipe = get_object_or_404(Recipe.objects.filter(id=id))
    return render(request, 'recipes/pages/recipe-view.html', context={'recipe': recipe, 'is_detail_page': True})
