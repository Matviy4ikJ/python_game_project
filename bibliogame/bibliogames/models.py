from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    developer = models.ForeignKey('Developer', on_delete=models.CASCADE)
    genres = models.ManyToManyField('Genre')
    platforms = models.ManyToManyField('Platforms')
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    class Meta:
        ordering = ['-release_date']
        db_table = 'games'

    def __str__(self):
        return self.name


class Developer(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(null=True, blank=True)


class Genre(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']


class Platforms(models.Model):
    name = models.CharField(max_length=100)

