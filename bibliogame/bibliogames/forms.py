from django import forms
from bibliogames.models import Game, Review, Developer


class GameCreateForm(forms.ModelForm):
    developer_name = forms.CharField(
        required=False,
        label="Developer Name",
        widget=forms.TextInput(attrs={"placeholder": "Enter developer name", "class": "form-control"})
    )
    developer_website = forms.URLField(
        required=False,
        label="Developer Website",
        widget=forms.URLInput(attrs={"placeholder": "Enter developer website (optional)", "class": "form-control"})
    )

    class Meta:
        model = Game
        fields = [
            "title",
            "description",
            "release_date",
            "genres",
            "platforms",
            "cover_image"
        ]

        labels = {
            "title": "Game Title",
            "description": "Description",
            "release_date": "Release Date",
            "genres": "Genres",
            "platforms": "Platforms",
            "cover_image": "Cover Image",
        }

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter game title", "class": "form-control"}),
            "description": forms.Textarea(attrs={"placeholder": "Describe the game", "class": "form-control", "rows": 5}),
            "release_date": forms.DateInput(attrs={"placeholder": "YYYY-MM-DD", "class": "form-control"}),
            "genres": forms.CheckboxSelectMultiple(),
            "platforms": forms.CheckboxSelectMultiple(),
            "cover_image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        name = self.cleaned_data.get("developer_name")
        website = self.cleaned_data.get("developer_website")

        if name:
            developer, _ = Developer.objects.get_or_create(
                name__iexact=name.strip(),
                defaults={"name": name.strip(), "website": website}
            )
            instance.developer = developer

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=Review.RATING_CHOICES),
            'comment': forms.Textarea(attrs={'class': 'form-control',
                    'placeholder': 'Write your review...',
                    'rows': 4
                })
        }
<<<<<<< HEAD
>>>>>>> cdf141a (registered new models)
=======

>>>>>>> 96b2f5e (debug)
