import os
import django
import pytest

from django.contrib.auth.models import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_settings.settings")
django.setup()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        password="testpass",
        email="testmail@example.com"
    )


@pytest.fixture
def super_user():
    return User.objects.create_superuser(
        username="test_superuser",
        password="1234"
    )