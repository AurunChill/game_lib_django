# Django imports
import django
from django.contrib.auth import get_user_model

# Third-party imports
from dotenv import load_dotenv

# Standard imports
import os
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve() / '.env')


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

User = get_user_model()

username = os.getenv('DJANGO_SUPERUSER_USERNAME')
email = os.getenv('DJANGO_SUPERUSER_EMAIL')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')


if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
