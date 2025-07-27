from django import forms
from bibliogames.models import Game


class GameCreateForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ["title", "description", "release_date", "developer", "genres", "platforms", "cover_image"]

        labels = {"title": "Game Title",
                  "description": "Game Description",
                  "release_date": "Game Creation Date",
                  "developer": "Developer",
                  "genres": "Genre",
                  "platforms": "Platforms",
                  "cover_image": "Cover Image"}

        widgets = {
            "release_date": forms.DateInput(attrs={"placeholder":"year-month-day"}),
            "title": forms.TextInput(attrs={"placeholder": "Enter game title"}),
            "description": forms.Textarea(attrs={"placeholder":"Describe the game"}),
            "developer": forms.TextInput(attrs={"placeholder": "Enter game developer", "class": "form-control"}),
            "genres": forms.SelectMultiple(attrs={"class": "form-control"}),
            "platforms": forms.SelectMultiple(attrs={"class": "form-control"}),
            "cover_image": forms.ClearableFileInput(attrs={"class": "form-control"})
        }

    def save(self, commit=True):
        new_dev_name = self.cleaned_data.get("")