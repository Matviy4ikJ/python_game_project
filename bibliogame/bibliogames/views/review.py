from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Game, Review
from ..forms import ReviewForm


@login_required
def add_review(request, game_id):
    game = get_object_or_404(Game, id=game_id, status='approved')

    try:
        existing_review = Review.objects.get(user=request.user, game=game)

