import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bibliogames.models import Game, Developer, Genre, Platforms, Review, Favorites, FavoriteGame

fake = Faker()


class Command(BaseCommand):
    help = 'Seed database with fake games, reviews, and favorites'

    def handle(self, *args, **options):
        self.stdout.write("Clearing DB")
        Game.objects.all().delete()
        Developer.objects.all().delete()
        Review.objects.all().delete()
        Favorites.objects.all().delete()
        FavoriteGame.objects.all().delete()

        self.stdout.write("Creating genres and platforms")
        genres = [Genre.objects.get_or_create(name=name)[0] for name in [
            'Action', 'Adventure', 'RPG', 'Strategy', 'Horror', 'Indie'
        ]]
        platforms = [Platforms.objects.get_or_create(name=name)[0] for name in [
            'PC', 'PlayStation', 'Xbox', 'Switch', 'Linux'
        ]]

        self.stdout.write("Creating users")
        users = [User.objects.create_user(username=f"user{i}", password="test12345") for i in range(5)]

        self.stdout.write("Creating developers")
        devs = [Developer.objects.create(name=fake.company(), website=fake.url()) for _ in range(5)]

        self.stdout.write("Creating games")
        games = []
        for _ in range(30):
            game = Game.objects.create(
                title=fake.sentence(nb_words=3),
                description=fake.text(max_nb_chars=300),
                release_date=fake.date_between(start_date='-10y', end_date='today'),
                developer=random.choice(devs),
                status=random.choice(['pending', 'approved', 'rejected']),
            )
            game.genres.set(random.sample(genres, k=random.randint(1, 3)))
            game.platforms.set(random.sample(platforms, k=random.randint(1, 2)))
            games.append(game)

        self.stdout.write("Adding reviews")
        for game in games:
            reviewers = random.sample(users, k=random.randint(1, len(users)))
            for user in reviewers:
                Review.objects.create(
                    user=user,
                    game=game,
                    rating=random.randint(1, 5),
                    comment=fake.sentence(),
                )

        self.stdout.write("Adding games to favorites")
        for user in users:
            fav = Favorites.objects.create(user=user)
            fav_games = random.sample(games, k=random.randint(2, 5))
            for game in fav_games:
                FavoriteGame.objects.create(favorites=fav, game=game)

        self.stdout.write(self.style.SUCCESS("BD successfully loaded with data"))