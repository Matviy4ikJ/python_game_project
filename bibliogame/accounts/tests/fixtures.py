import pytest
from accounts.models import Profile


@pytest.fixture
def profile(user):
    return Profile.objects.create(user=user)