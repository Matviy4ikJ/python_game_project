from django.shortcuts import render, get_object_or_404

from django.db.models import Avg

from ..models import Game, Platforms, Developer, Genre, Favorites


def index(request):
    games = Game.objects.filter(status='approved')

    genre_id = request.GET.get('genre')
    platform_id = request.GET.get('platform')
    developer_id = request.GET.get('developer')
    search_query = request.GET.get('search')
    sort_option = request.GET.get('sort')

    if search_query:
        games = games.filter(title__icontains=search_query)

    if genre_id:
        games = games.filter(genres__id=genre_id)

    if platform_id:
        games = games.filter(platforms__id=platform_id)

    if developer_id:
        games = games.filter(developer__id=developer_id)

    match sort_option:
        case "rating_high":
            games = games.annotate(avg_rating=Avg("reviews__rating")).order_by("-avg_rating")
        case "rating_low":
            games = games.annotate(avg_rating=Avg("reviews__rating")).order_by("avg_rating")
        case "release_new":
            games = games.order_by('-release_date')
        case "release_old":
            games = games.order_by('release_date')


    if request.user.is_authenticated:
        try:
            favorites = request.user.favorites
            favorite_game_ids = set(fg.game.id for fg in favorites.games.all())
        except Favorites.DoesNotExist:
            favorite_game_ids = set()
    else:
        favorite_game_ids = set()

    context = {
        'games': games,
        'genres': Genre.objects.all(),
        'platforms': Platforms.objects.all(),
        'developers': Developer.objects.all(),
        'selected_genre': int(genre_id) if genre_id else None,
        'selected_platform': int(platform_id) if platform_id else None,
        'selected_developer': int(developer_id) if developer_id else None,
        'search_query': search_query or '',
        'sort_option': sort_option or '',
        'favorite_game_ids': favorite_game_ids, 
    }

    return render(request, 'index.html', context)


def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk, status='approved')
    reviews = game.reviews.select_related('user').all()

    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    return render(request, 'game_detail.html', {
        'game': game,
        'reviews': reviews,
        'user_review': user_review,
    })
<<<<<<< HEAD
>>>>>>> 096ca5e (Reviews)
=======
>>>>>>> 96b2f5e (debug)
