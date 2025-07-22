import pytest
from django.urls import reverse
from django.test import Client
import datetime
from bibliogames.models import FavoriteGame, Favorites
from .fixtures import game, developer, genres, platforms, favorite_game


@pytest.mark.django_db
def test_user_game_creation_for_moderate(client, game, user, developer, genres, platforms):
    client.force_login(user=user)

    data = {
        "title": "test_game",
        "description": "test_description",
        "release_date": "2013-08-12",
        "developer": developer.id,
        "genres": [genre.id for genre in genres],
        "platforms": [platform.id for platform in platforms]
    }

    url = reverse("bibliogames:create_game")
    response = client.post(url, data=data, format="json")

    assert response.status_code == 302


@pytest.mark.django_db
def test_game_delete_by_moderator(user, client, game):
    user.is_staff = True
    user.save()

    client.force_login(user=user)

    url = reverse("bibliogames:delete_game", args=[game.id])

    response = client.delete(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_game_moderate_action_approved(user, client, game):
    user.is_staff = True
    user.save()

    client.force_login(user=user)

    url = reverse("bibliogames:moderate_game", args=[game.id, "approve"])

    response = client.post(url)

    assert response.status_code == 302

    game.refresh_from_db()
    assert game.status == "approved"


@pytest.mark.django_db
def test_game_moderate_action_rejected(user, client, game):
    user.is_staff = True
    user.save()

    client.force_login(user=user)

    url = reverse("bibliogames:moderate_game", args=[game.id, "reject"])

    response = client.post(url)

    assert response.status_code == 302

    game.refresh_from_db()
    assert game.status == "rejected"


@pytest.mark.django_db
def test_game_moderation_list(user, client, game):

    user.is_staff = True
    user.save()

    client.force_login(user=user)

    url = reverse("bibliogames:moderation_list")
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_add_favorite_game_authenticated(user, client, game, favorite_game):
    client.force_login(user=user)

    url = reverse("bibliogames:add_favorite_game", args=[game.id])
    response = client.post(url, favorite_game=favorite_game, format="json")

    assert response.status_code == 302
    assert FavoriteGame.objects.filter(favorites=user.favorites, game=game).exists()


@pytest.mark.django_db
def test_add_favorite_game_not_authenticated(user, client, game, favorite_game):
    url = reverse("bibliogames:add_favorite_game", args=[game.id])
    response = client.post(url, favorite_game=favorite_game, format="json")

    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_favorite_game_authenticated(user, client, game, favorite_game):
    client.force_login(user=user)

    url = reverse("bibliogames:delete_favorite_game", args=[game.id])
    response = client.delete(url, favorite_game=favorite_game, format="json")

    assert response.status_code == 302
    assert not FavoriteGame.objects.filter(favorites=user.favorites, game=game).exists()


@pytest.mark.django_db
def test_delete_favorite_game_not_authenticated(user, client, game, favorite_game):
    session = client.session
    session["favorite_games"] = {game.id: True}
    session.save()

    url = reverse("bibliogames:delete_favorite_game", args=[game.id])
    response = client.delete(url)

    assert response.status_code == 302

    session = client.session
    assert game.id not in session.get("favorite_games", {})