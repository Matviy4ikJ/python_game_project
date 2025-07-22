from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from bibliogames.models import Game


@staff_member_required
def moderation_list(request):
    games = Game.objects.filter(status='pending')
    return render(request, 'moderation/list.html', {'games': games})


@staff_member_required
def moderate_game(request, game_id, action):
    game = get_object_or_404(Game, id=game_id)

    if action == 'approve':
        game.status = 'approved'
    elif action == 'reject':
        game.status = 'rejected'
    else:
        return redirect("bibliogames:moderation_list")
    game.save()
    return redirect("bibliogames:moderation_list")


@staff_member_required()
def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    game.delete()
    return redirect("accounts:profile_view")
