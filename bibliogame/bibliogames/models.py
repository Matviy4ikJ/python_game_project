from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На перевірці'),
        ('approved', 'Схвалено'),
        ('rejected', 'Відхилено'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    developer = models.ForeignKey("Developer", on_delete=models.CASCADE)
    genres = models.ManyToManyField("Genre")
    platforms = models.ManyToManyField("Platforms")
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, default=0.0)
    cover_image = models.ImageField(upload_to='game_covers/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-release_date']
        db_table = 'games'

    def str(self):
        return self.title


class Developer(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(null=True, blank=True)


class Genre(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']


class Platforms(models.Model):
    name = models.CharField(max_length=100)


class Favorites(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)


class FavoriteGame(models.Model):
    favorites = models.ForeignKey(Favorites, on_delete=models.CASCADE, related_name="games")
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("favorites", "game")