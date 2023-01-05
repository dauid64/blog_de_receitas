from pathlib import Path
from utils.environment import get_env_variable, parse_comma_str_to_list
import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECURE')

DEBUG = True if os.environ.get('DEBUG') == '1' else False

ALLOWED_HOSTS = parse_comma_str_to_list(
    get_env_variable('ALLOWED_HOSTS')
    )
CSRF_TRUSTED_ORIGINS = parse_comma_str_to_list(
    get_env_variable('CSRFF_TRUSTED_ORIGINS ')
)

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
