from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class SearchViewsTest(RecipeTestBase):
    def test_search_view_function_is_correct(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)

    def test_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?search=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_search_term_is_on_page_title_and_escaped(self):
        response = self.client.get(reverse('recipes:search') + '?search=<teste>')
        self.assertIn('Search for &quot;&lt;teste&gt;&quot;', response.content.decode('utf-8'))
