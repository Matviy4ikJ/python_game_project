from django.shortcuts import render, get_object_or_404
from ..models import Game, Platforms, Developer, Genre


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
            games = games.order_by('-rating')
        case "rating_low":
            games = games.order_by('rating')
        case "release_new":
            games = games.order_by('-release_date')
        case "release_old":
            games = games.order_by('release_date')

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
    }

    return render(request, 'games/index.html', context)


def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk, status='approved')
    return render(request, 'games/game_detail.html', {'game': game})

