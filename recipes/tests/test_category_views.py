from django.urls import resolve, reverse

from recipes import views
from .test_recipe_base import RecipeTestBase


class CategoryViewsTest(RecipeTestBase):
    def test_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_category_view_return_status_code_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 404)

    def test_category_template_loads_recipes(self):
        needed_title = 'This is a category test'

        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))      # noqa: E501
        response_content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, response_content)

    def test_category_template_dont_load_recipes_not_published(self):
        '''Test recipe is_published False dont show'''
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': recipe.category.id}))    # noqa: E501

        self.assertEqual(response.status_code, 404)
