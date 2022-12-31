from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from django.urls import reverse


class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )

    def login(self, user_exist=False, username='my_user', password='my_pass'):
        if not user_exist:
            User.objects.create_user(
                    username=username,
                    password=password
                )
        # Usuário abrea a pagina de login
        self.browser.get(self.live_server_url + reverse('authors:login'))
        # Usuário vê o formulário de login
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')
        # Usuário digita seu usuário e senha
        username_field.send_keys(username)
        password_field.send_keys(password)
        # Usuário envia o furmulário
        form.submit()

