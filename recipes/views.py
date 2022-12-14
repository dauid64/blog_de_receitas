from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.db.models import Q
from django.http import Http404
from recipes.models import Recipe


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={'recipes': recipes})     # noqa: E501


def category(request, category_id):
    # recipes = Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id') # category_id é igual ao category_id da recipes # noqa: E501
    recipes = get_list_or_404(Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id'))   # noqa: E501
    return render(request, 'recipes/pages/category.html', context={'recipes': recipes, 'title': recipes[0].category.name})  # noqa: E501


def recipe(request, id):
    # recipe = Recipe.objects.filter(id=id)
    recipe = get_object_or_404(Recipe.objects.filter(id=id, is_published=True))
    return render(request, 'recipes/pages/recipe-view.html', context={'recipe': recipe, 'is_detail_page': True})    # noqa: E501


def search(request):
    search_term = request.GET.get('search', '').strip()
    if not search_term:
        raise Http404()
    recipes = Recipe.objects.filter(Q(Q(title__icontains=search_term) | Q(description__icontains=search_term)), is_published=True).order_by('-id')
    return render(request, 'recipes/pages/search.html', {'page_title': f'Search for "{search_term}"', 'recipes': recipes})
