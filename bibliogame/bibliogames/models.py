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
    cover_image = models.ImageField(upload_to='game_covers/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0.0

    class Meta:
        ordering = ['-release_date']
        db_table = 'games'

    def __str__(self):
        return self.title


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} — {self.game.title} — {self.rating}★"


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


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} — {self.game.title} — {self.rating}★"
