import pytest
import datetime
from django.contrib.auth.models import User
from bibliogames.models import Game, Developer, Genre, Platforms, Favorites, FavoriteGame, Review
from .fixtures import game


@pytest.mark.django_db
def test_game_model():
    developer = Developer.objects.create(name="test_developer", website="test_website")
    genres = Genre.objects.create(name="test_genres")
    platforms = Platforms.objects.create(name="test_platforms")

    game = Game.objects.create(title="test_game",
                               description="test_description",
                               release_date=datetime.date(2013, 8, 12),
                               developer=developer
                               )

    game.genres.add(genres)
    game.platforms.add(platforms)

    assert genres in game.genres.all()
    assert genres.name == "test_genres"
    assert developer.website == "test_website"


# @pytest.mark.django_db
# def test_favorite_model(user, game):
#     favorite = FavoriteGame.objects.create(favorites=user.favorites,
#                                            game=game)
#
#     assert user.favorite == game
#     assert favorite.created_at is not None


@pytest.mark.django_db
def test_review_model(user, game):
    review = Review.objects.create(
        user=user,
        game=game,
        rating=3
    )

    assert review.rating == 3
    assert review.created_at is not None
