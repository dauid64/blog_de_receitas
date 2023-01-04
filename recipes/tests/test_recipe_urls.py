from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_home_url_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_category_url_is_correct(self):
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/recipes/category/1/')

    def test_recipe_url_is_correct(self):
        url = reverse('recipes:recipe', kwargs={'pk': 1})
        self.assertEqual(url, '/recipes/1/')

    def test_search_url_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')
