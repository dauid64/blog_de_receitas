from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
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
        self.make_recipe(author_data={'first_name': 'joaozinho'})
        response = self.client.get(reverse('recipes:home'))
        response_content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        self.assertIn('Recipe Title', response_content)
        self.assertIn('10 Minutos', response_content)
        self.assertIn('joaozinho', response_content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_category_view_return_status_code_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_view_return_status_code_404_if_no_recipe_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)
