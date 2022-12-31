import pytest
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsDashboardCreateTest(AuthorsBaseTest):
    def go_to_dashboard_create(self):
        link = reverse('authors:dashboard_recipe_create')
        create_recipe = self.browser.find_element(
            By.XPATH, f'//a[@href="{link}"]')
        create_recipe.click()

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div/div[2]/div/form'
        )

    def test_dashborad_create_field_preparationsteps_and_cover_class_span2(self):
        self.login()
        self.go_to_dashboard_create()

        self.assertIn(
            'Preparation steps',
            self.browser.find_elements(By.CLASS_NAME, 'span-2')[0].text
        )
        self.assertIn(
            'Cover',
            self.browser.find_elements(By.CLASS_NAME, 'span-2')[2].text
        )

    def test_dashboard_create_recipe_successfully(self):
        self.login()
        self.go_to_dashboard_create()

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        title_field = self.get_by_placeholder(form, 'Your recipe title')
        description_field = self.get_by_placeholder(
            form, 'Description of your recipe')
        preparation_time_field = self.get_by_placeholder(
            form, 'How long does it take')
        servings_field = self.get_by_placeholder(form, 'The amount')
        preparation_steps_field = form.find_element(
            By.XPATH,
            '//textarea[@placeholder="Your recipe"]'
        )

        title_field.send_keys('title')
        description_field.send_keys('description')
        preparation_time_field.send_keys('2')
        servings_field.send_keys('3')
        preparation_steps_field.send_keys('preparation steps')

        form.submit()

        self.assertIn(
            'Sua receita foi salva com sucesso!',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
