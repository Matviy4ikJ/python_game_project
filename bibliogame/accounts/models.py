from django.db import models
from django.contrib.auth.models import User

from bibliogames.models import Game

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to="avatars/", default="avatars/default_avatar.png", blank=True
    )
    favorites = models.ManyToManyField(Game, related_name='favorited_by', blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"




