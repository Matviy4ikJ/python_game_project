from django import forms
from bibliogames.models import Game


class GameCreateForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ["title", "description", "release_date", "developer", "genres", "platforms", "cover_image"]

        labels = {"title": "game title",
                  "description": "game description",
                  "release_date": "game creation date",
                  "developer": "game developer",
                  "genres": "game genres",
                  "platforms": "game platforms",
                  "cover_image": "game icon"}