import random
from faker import Faker
from django.core.management.base import BaseCommand
from ...models import Game, Developer, Genre, Platforms


class Command(BaseCommand):
    help = 'generate test db data'

    def handle(self, *args, **options):
        fake = Faker()

        genres_list = ['Action', 'Adventure', 'RPG', 'Simulation', 'Strategy', 'Horror', 'Puzzle', 'Milsim']
        platforms_list = ['PC', 'PlayStation 4', 'PlayStation 3', 'PlayStation 2', 'Xbox One', 'Nintendo Switch']
        statuses = ['pending', 'approved', 'rejected']

        genre_objs = [Genre.objects.get_or_create(name=genre)[0] for genre in genres_list]
        platform_objs = [Platforms.objects.get_or_create(name=plat)[0] for plat in platforms_list]

        Game.objects.all().delete()

        for _ in range(30):
            developer_name = fake.company()
            developer, _ = Developer.objects.get_or_create(name=developer_name, defaults={
                'website': fake.url()
            })

            game = Game.objects.create(
                title=fake.sentence(nb_words=3),
                description=fake.text(max_nb_chars=200),
                release_date=fake.date_between(start_date='-5y', end_date='today'),
                developer=developer,
                rating=round(random.uniform(1.0, 5.0), 1),
                status=random.choice(statuses),
            )

            game.genres.set(random.sample(genre_objs, k=random.randint(1, 3)))
            game.platforms.set(random.sample(platform_objs, k=random.randint(1, 2)))

        self.stdout.write(self.style.SUCCESS('Successfully added 30 test games!'))
