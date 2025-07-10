from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from ..forms import GameCreateForm
from bibliogames.models import Game


def create_game(request):
    if request.method == "POST":
        form = GameCreateForm(request.POST)
        if form.is_valid():
            game = form.save()
            game.save()
            return redirect("")

    else:
        form = GameCreateForm()
    return render(request, "", context={"form": form})


def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.user.is_superuser():
        game.delete()
        return redirect("")
    else:
        return HttpResponseForbidden("you can't delete the game because you don't have rights")


