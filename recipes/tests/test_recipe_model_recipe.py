from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(category=self.make_category(name='Test default Category'), author=self.make_author(username='newuser'), title='Recipe Title Test', description='Recipe Description', slug='recipe-slug-for-no-defatults', preparation_time=10, preparation_time_unit='Minutos', servings=5, servings_unit='Porções', preparation_steps='Recipe preparation Steps')      # noqa: E501
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([('title', 65), ('description', 165), ('preparation_time_unit', 65), ('servings_unit', 65)])      # noqa: E501
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_defalt(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.preparation_steps_is_html, msg='Recipe preparation steps html is not False')    # noqa: E501

    def test_recipe_is_published_is_false_by_defalt(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.is_published, msg='Recipe is_published is not False')   # noqa: E501

    def test_recipe_str_representation(self):
        needed = 'Testing Representation'
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'Testing Representation',
                         msg=f"Recipe string representation must be {needed}")

    def test_recipe_if_slug_is_none_autofill(self):
        self.recipe.slug = ''
        self.recipe.full_clean()
        self.recipe.save()
        self.assertIn('recipe-title', self.recipe.slug)
