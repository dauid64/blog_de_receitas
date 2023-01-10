import time

import pytest
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By

from recipes.tests.test_recipe_base import RecipeMixin
from django.test import override_settings
from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsDashboardDeleteTest(AuthorsBaseTest, RecipeMixin):

    @override_settings(DEBUG=True)
    def test_delete_recipe_successfully(self):
        self.make_recipe(is_published=False)
        self.login(True, username='username', password='123456')
        button = self.browser.find_element(By.CLASS_NAME, 'button-delete')
        button.click()
        alert = Alert(self.browser)
        alert.accept()
        self.assertIn(
            'Deleted successfully',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
