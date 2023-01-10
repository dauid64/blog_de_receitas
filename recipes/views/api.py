from rest_framework.decorators import api_view
from rest_framework.response import Response
from recipes.models import Recipe
from ..serializers import RecipeSerializer
from django.shortcuts import get_object_or_404


@api_view()
def recipe_api_list(request):
    recipes = Recipe.objects.get_published()
    seriealizer = RecipeSerializer(instance=recipes, many=True)
    return Response(seriealizer.data)


@api_view()
def recipe_api_detail(request, pk):
    recipes = get_object_or_404(
        Recipe.objects,
        pk=pk
    )
    serializer = RecipeSerializer(instance=recipes)
    return Response(serializer.data)
