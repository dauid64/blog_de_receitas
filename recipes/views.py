from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.db.models import Q
from django.http import Http404
from recipes.models import Recipe
from utils.pagination import make_pagination
import os

PER_PAGE = int(os.environ.get('PER_PAGE', 6))

def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    return render(request, 'recipes/pages/home.html', context={'recipes': page_obj, 'pages': pagination_range})     # noqa: E501


def category(request, category_id):
    # recipes = Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id') # category_id é igual ao category_id da recipes # noqa: E501
    recipes = get_list_or_404(Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id'))   # noqa: E501
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    return render(request, 'recipes/pages/category.html', context={'recipes': page_obj, 'title': recipes[0].category.name, 'pages': pagination_range})  # noqa: E501


def recipe(request, id):
    # recipe = Recipe.objects.filter(id=id)
    recipe = get_object_or_404(Recipe.objects.filter(id=id, is_published=True))
    return render(request, 'recipes/pages/recipe-view.html', context={'recipe': recipe, 'is_detail_page': True})    # noqa: E501


def search(request):
    search_term = request.GET.get('search', '').strip()
    if not search_term:
        raise Http404()
    recipes = Recipe.objects.filter(Q(Q(title__icontains=search_term) | Q(description__icontains=search_term)), is_published=True).order_by('-id')
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    return render(request, 'recipes/pages/search.html', {'page_title': search_term, 'recipes': page_obj, 'pages': pagination_range, 'additional_url_query': f'&search={search_term}'})