from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from ..forms import GameCreateForm
from bibliogames.models import Game, Favorites, FavoriteGame
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def create_game(request):
    if request.user.is_superuser():
        if request.method == "POST":
            form = GameCreateForm(request.POST)
            if form.is_valid():
                game = form.save()
                game.save()
                return redirect("")
        else:
            form = GameCreateForm()

    else:
        return HttpResponseForbidden("you can't add the game because you don't have rights")

    return render(request, "", context={"form": form})


def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.user.is_superuser():
        game.delete()
        return redirect("")
    else:
        return HttpResponseForbidden("you can't delete the game because you don't have rights")


def add_favorite_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if not request.user.is_authenticated():
        favorites = request.session.get(settings.FAVORITE_SESSION_ID, {})
        request.session[settings.FAVORITE_SESSION_ID] = favorites
    else:
        favorites = request.user.favorites
        favorite_game = FavoriteGame.objects.get_or_create(favorites=favorites, game=game)
        favorite_game.save()
    return redirect("")


def delete_favorite_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if not request.user.is_authenticated():
        favorites = request.session.get(settings.FAVORITE_SESSION_ID, {})
        if game_id in favorites:
            del favorites[game_id]
            request.session[settings.FAVORITE_SESSION_ID] = favorites
    else:
        try:
            favorites = request.user.favorites
            game_del = FavoriteGame.objects.get(favorites=favorites, game=game)
            game_del.delete()
        except FavoriteGame.DoesNotExist:
            favorites = None
    return redirect("")
