from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms import AuthorRecipeForm


class AuthorDashboardCreateTest(TestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'title': 'title',
            'description': 'description',
            'preparation_time': '2',
            'servings': '1',
            'preparation_steps': 'preparation steps',
        }
        return super().setUp(*args, **kwargs)

    def login(self, username='my_user', password='my_pass'):
        User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)

    @parameterized.expand([
        ('title', 'Your recipe title'),
        ('description', 'Description of your recipe'),
        ('preparation_time', 'How long does it take'),
        ('servings', 'The amount'),
        ('preparation_steps', 'Your recipe')
    ])
    def test_fields_placeholders(self, field, placeholder):
        form = AuthorRecipeForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    def test_user_set_title_with_less_5_characters(self):
        self.login()
        self.form_data['title'] = 'abc'
        url = reverse('authors:dashboard_recipe_create')
        response = self.client.post(
            url,
            data=self.form_data,
            follow=True
        )
        self.assertIn(
            'Title must have at least 5 characters.',
            response.content.decode('utf-8')
        )

    def test_user_set_title_and_description_equal(self):
        self.login()
        self.form_data['title'] = 'a' * 5
        self.form_data['description'] = 'a' * 5
        url = reverse('authors:dashboard_recipe_create')
        response = self.client.post(
            url,
            data=self.form_data
        )
        self.assertIn(
            'Cannot be equal to description',
            response.content.decode('utf-8')
        )

    def test_user_set_number_negative_in_preaparation_time(self):
        self.login()
        self.form_data['preparation_time'] = '-2'
        url = reverse('authors:dashboard_recipe_create')
        response = self.client.post(
            url,
            data=self.form_data
        )
        self.assertIn(
            'Must be a positive number',
            response.content.decode('utf-8')
        )

    def test_user_set_number_negative_in_servings(self):
        self.login()
        self.form_data['servings'] = '-2'
        url = reverse('authors:dashboard_recipe_create')
        response = self.client.post(
            url,
            data=self.form_data
        )
        self.assertIn(
            'Must be a positive number',
            response.content.decode('utf-8')
        )

    def test_user_get_recipe_if_id_not_exist_return_error_404(self):
        self.login()
        response = self.client.get(
            reverse(
                'authors:dashboard_recipe_edit',
                kwargs={'id': 1}
                )
            )
        self.assertEqual(response.status_code, 404)
