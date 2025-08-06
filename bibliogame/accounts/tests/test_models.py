import pytest
from django.contrib.auth.models import User
from accounts.models import Profile


@pytest.mark.django_db
def test_profile_model(user):
    Profile.objects.create(user=user)

    assert user.username == "testuser"