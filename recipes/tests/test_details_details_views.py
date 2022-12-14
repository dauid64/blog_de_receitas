from django.urls import resolve, reverse

from recipes import views
from .test_recipe_base import RecipeTestBase


class DetailsViewsTest(RecipeTestBase):
    def test_details_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_details_view_return_status_code_404_if_no_recipe_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)

    def test_details_template_loads_recipes(self):
        needed_title = 'This is a detail page - It load one recipe'

        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        response_content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, response_content)

    def test_details_template_dont_load_recipe_not_published(self):
        '''Test recipe is_published False dont show'''
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': recipe.id}))     # noqa: E501

        self.assertEqual(response.status_code, 404)
