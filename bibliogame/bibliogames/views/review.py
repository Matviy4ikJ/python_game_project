from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from ..models import Game, Review
from ..forms import ReviewForm


@login_required
def add_review(request, game_id):
    game = get_object_or_404(Game, id=game_id, status='approved')

    try:
        existing_review = Review.objects.get(user=request.user, game=game)
        messages.warning(request, 'You have already left a review for this game.')
        return redirect('game_detail', game_id=game.id)
    except Review.DoesNotExist:
        pass

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.game = game
            review.save()
            messages.success(request, 'Review added successfully')
            return redirect('game_detail', game_id=game.id)
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'form': form, 'game': game})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return HttpResponseForbidden('You can delete only your review')

    game_id = review.game.id
    review.delete()
    messages.success(request, 'Review deleted successfully')
    return redirect('game_detail', game_id=game_id)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            updated_review = form.save(commit=False)
            updated_review.is_approved = False
            updated_review.save()
            messages.success(request, 'Your review has been updated and sent for re-approval.')
            return redirect('game_detail', pk=review.game.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/edit_review.html', {'form': form, 'game': review.game})
