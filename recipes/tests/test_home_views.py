from django.urls import resolve, reverse

from recipes import views
from .test_recipe_base import RecipeTestBase


class HomeViewsTest(RecipeTestBase):
    def test_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_load_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_home_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found', response.content.decode('utf-8'))

    def test_home_template_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe(author_data={'first_name': 'joaozinho'})

        response = self.client.get(reverse('recipes:home'))
        response_content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Check if one recipe exists
        self.assertIn('Recipe Title', response_content)
        self.assertIn('10 Minutos', response_content)
        self.assertIn('joaozinho', response_content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_home_template_dont_load_recipes_not_published(self):
        '''Test recipe is_published False dont show'''
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))
        response_content = response.content.decode('utf-8')

        self.assertIn('No recipes found', response_content)
