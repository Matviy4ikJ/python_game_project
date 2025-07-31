import pytest
from django.urls import reverse
from django.test import Client
import datetime

from bibliogames.models import FavoriteGame, Favorites, Review
from .fixtures import game, developer, genres, platforms, favorite_game, review


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

    assert response.status_code == 200


@pytest.mark.django_db
def test_not_authenticated_user_game_creation_for_moderate(client, game, user, developer, genres, platforms):
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

    assert response.status_code == 403


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
def test_game_moderate_action_invalid(user, client, game, super_user):
    client.force_login(user=super_user)

    url = reverse("bibliogames:moderate_game", args=[game.id, "invalid"])

    response = client.post(url)

    assert response.status_code == 302

    game.refresh_from_db()
    assert game.status != "approved"
    assert game.status != "rejected"
    

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


@pytest.mark.django_db
def test_edit_game(super_user, client, game, developer, genres, platforms):
    client.force_login(user=super_user)

    data = {
        "title": "test_new_game",
        "description": "test_new_description",
        "release_date": "2002-04-18",
        "developer": developer.id,
        "genres": [genre.id for genre in genres],
        "platforms": [platform.id for platform in platforms]
    }

    url = reverse("bibliogames:edit_game", args=[game.id])

    response = client.post(url, data=data, format="json")
    assert response.status_code == 200
    assert data["title"] == "test_new_game"
    assert data["description"] == "test_new_description"
    assert data["release_date"] == "2002-04-18"


@pytest.mark.django_db
def test_add_review(client, user, game):
    client.force_login(user=user)

    game.status = 'approved'
    game.save()

    url = reverse("bibliogames:add_review", args=[game.id])
    data = {"rating":5, "comment": "ttt"}

    response = client.post(url, data)

    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_review(client, user, review):
    client.force_login(user=user)

    url = reverse("bibliogames:delete_review", args=[review.id])
    response = client.delete(url)

    assert response.status_code == 302


@pytest.mark.django_db
def test_edit_review(client, user, game, review):
    client.force_login(user)

    url = reverse("bibliogames:edit_review", args=[review.id])
    response = client.post(url, {
        "rating": 5,
        "comment": "Updated comment"
    })

    assert response.status_code == 302
    review.refresh_from_db()
    assert review.rating == 5
    assert review.comment == "Updated comment"