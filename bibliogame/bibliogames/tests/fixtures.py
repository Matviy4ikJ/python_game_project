import pytest
import datetime
from bibliogames.models import Game, Developer, Genre, Platforms, Favorites, FavoriteGame


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
