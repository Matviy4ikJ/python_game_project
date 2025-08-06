from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from bibliogames.models import Game
from bibliogames.forms import GameEditForm


@staff_member_required
def moderation_list(request):
    status = request.GET.get('status', 'pending')
    if status not in ['pending', 'approved']:
        status = 'pending'
    
    games = Game.objects.filter(status=status)
    
    context = {
        'games': games,
        'current_status': status,
    }
    return render(request, 'moderation/list.html', context)


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


@staff_member_required
def edit_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.method == "POST":
        form = GameEditForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            return redirect('bibliogames:game_detail', pk=game.id)
    else:
        form = GameEditForm(instance=game)

    return render(request, 'moderation/edit_game.html', {'form': form, 'game': game})


@staff_member_required()
def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    game.delete()
    return redirect("accounts:profile_view")


@staff_member_required()
def moderate_game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id, status__in=['pending', 'approved'])
    return render(request, 'moderation/moderation_game_detail.html', {'game': game})
