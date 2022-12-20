from django.urls import resolve, reverse

from .test_recipe_base import RecipeTestBase


class PaginationTest(RecipeTestBase):
    def make_recipes_for_pagination(self, numbers):
        for i in range(numbers):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

    def test_pagination_dont_is_numeric(self):
        response = self.client.get(reverse('recipes:home') + '?page=A')
        pages = response.context['pages']  # response.context['recipes'].number
        self.assertEqual(1, pages['current_page'])

    def test_pagination_is_stop_range_correctly(self):
        self.make_recipes_for_pagination(27)
        response = self.client.get(reverse('recipes:home') + '?page=4')
        pages = response.context['pages']
        self.assertEqual(pages['pagination'], range(2,6))

    def test_pagination_is_start_range_correctly(self):
        self.make_recipes_for_pagination(27)
        response = self.client.get(reverse('recipes:home') + '?page=1')
        pages = response.context['pages']
        self.assertEqual(pages['pagination'], range(1,5))