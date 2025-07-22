import pytest
import datetime
from bibliogames.models import Game, Developer, Genre, Platforms, Favorites, FavoriteGame


@pytest.fixture
def developer():
    developer_ = Developer.objects.create(name="test_developer", website="test_website")

    return developer_


@pytest.fixture
def genres():
    return [
        Genre.objects.create(name="test_genre_1"),
        Genre.objects.create(name="test_genre_2"),
    ]


@pytest.fixture
def platforms():
    return [
        Platforms.objects.create(name="test_platform_1"),
        Platforms.objects.create(name="test_platform_2")
    ]


@pytest.fixture
def game():
    developer = Developer.objects.create(name="test_developer", website="test_website")
    genres = Genre.objects.create(name="test_genres")
    platforms = Platforms.objects.create(name="test_platforms")

    game_ = Game.objects.create(title="test_game",
                                description="test_description",
                                release_date=datetime.date(2013, 8, 12),
                                developer=developer
                                )

    game_.genres.add(genres)
    game_.platforms.add(platforms)

    return game_


@pytest.fixture
def favorite_game(user, game):
    favorites = Favorites.objects.create(user=user)

    favorite_game_ = FavoriteGame.objects.create(favorites=favorites,
                                                 game=game)

    return favorite_game_
