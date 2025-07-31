import pytest
from django.contrib.auth import get_user
from django.urls import reverse
from django.test import Client
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from .fixtures import profile


@pytest.mark.django_db
def test_register_view(profile, client):

    data = {"username": "testuser",
            "email": "testmail@example.com",
            "password1": "testpass",
            "password2": "testpass"}

    url = reverse("accounts:register")
    response = client.post(url, data, format="json")

    assert response.status_code == 200
    assert User.objects.filter(username="testuser").exists()


@pytest.mark.django_db
def test_login_view(profile, client):

    data = {"username": "testuser",
            "password": "testpass"}

    url = reverse("accounts:login")
    response = client.post(url, data)

    assert response.status_code == 302

    logged_user = get_user(client)
    assert logged_user.is_authenticated


@pytest.mark.django_db
def test_logout_view(client, user):
    client.force_login(user=user)

    url = reverse("accounts:logout")
    response = client.post(url)

    assert response.status_code == 302

    logout_user = get_user(client)
    assert not logout_user.is_authenticated


@pytest.mark.django_db
def test_profile_view(client, profile, user):
    client.force_login(user=user)

    url = reverse("accounts:profile")
    response = client.get(url)

    assert response.status_code == 200
    assert profile is not None


@pytest.mark.django_db
def test_confirm_email_view_if_not_email(client, profile):
    url = reverse("accounts:confirm_email")

    session = client.session
    session['register_form_data'] = {
        "username": "testuser2",
        "password1": "testpass2",
        "password2": "testpass2"
    }
    session.save()

    response = client.get(url)

    assert response.status_code == 400
    assert not User.objects.filter(username="testuser2").exists()


@pytest.mark.django_db
def test_confirm_email_view_if_email_exists(client, profile, user):
    url = reverse("accounts:confirm_email")

    session = client.session
    session['register_form_data'] = {
        "username": "testuser2",
        "password1": "testpass2",
        "password2": "testpass2"
    }
    session.save()

    response = client.get(url, {"email": "testmail@example.com"})

    assert response.status_code == 400
    assert not User.objects.filter(username="testuser2").exists()


@pytest.mark.django_db
def test_confirm_email_view_if_not_form_data(client, profile):
    url = reverse("accounts:confirm_email")

    session = client.session
    if 'register_form_data' in session:
        del session['register_form_data']
    session.save()

    response = client.get(url, {"email": "testmail@example.com"})

    assert response.status_code == 400
    assert 'register_form_data' not in session


@pytest.mark.django_db
def test_confirm_email_view(client, profile, user):
    url = reverse("accounts:confirm_email")

    session = client.session
    session['register_form_data'] = {
        "username": "testuser2",
        "password1": "testpass2",
        "password2": "testpass2"
    }
    session.save()

    response = client.get(url, {"email": "testmail2@example.com"})

    assert response.status_code == 200
    assert User.objects.filter(username="testuser2", email="testmail2@example.com").exists()
    session = client.session
    assert 'register_form_data' not in session


@pytest.mark.django_db
def test_edit_profile(client, profile, user):
    client.force_login(user=user)

    data = {"username": "updatetestuser",
            "email": "updatetestmail@example.com"}

    url = reverse("accounts:edit_profile")

    response = client.post(url, data=data, format="json")
    assert response.status_code == 302

    assert data['username'] == "updatetestuser"
    assert data['email'] == "updatetestmail@example.com"
    