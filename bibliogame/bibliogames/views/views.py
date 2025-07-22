from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from bibliogames.forms import GameCreateForm
from bibliogames.models import Game, Favorites, FavoriteGame


def create_game(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("First register to submit your game")

    if request.method == "POST":
        form = GameCreateForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.author = request.user
            game.status = 'pending'
            game.save()
            return redirect("accounts:profile_view")
    else:
        form = GameCreateForm()

    return render(request, "bibliogames/create_game.html", context={"form": form})


def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if not request.user.is_superuser:
        return HttpResponseForbidden("You can't delete the game because you don't have rights")

    game.delete()
    return redirect("accounts:profile_view")


def add_favorite_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if not request.user.is_authenticated:
        favorites = request.session.get(settings.FAVORITE_SESSION_ID, {})
        request.session[settings.FAVORITE_SESSION_ID] = favorites
    else:
        favorites = request.user.favorites
        favorite_game, created = FavoriteGame.objects.get_or_create(favorites=favorites, game=game)

    return redirect("accounts:profile_view")


def delete_favorite_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if not request.user.is_authenticated:
        favorites = request.session.get(settings.FAVORITE_SESSION_ID, {})
        if str(game_id) in favorites:
            del favorites[str(game_id)]
            request.session[settings.FAVORITE_SESSION_ID] = favorites
    else:
        try:
            favorites = request.user.favorites
            game_del = FavoriteGame.objects.get(favorites=favorites, game=game)
            game_del.delete()
        except FavoriteGame.DoesNotExist:
            pass

    return redirect("accounts:profile_view")


def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk, status='approved')
    return render(request, 'bibliogames/game_detail.html', {'game': game})
