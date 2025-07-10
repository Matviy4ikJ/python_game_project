from django.urls import path
from .views.views import create_game, delete_game, add_favorite_game, delete_favorite_game

app_name = "bibliogames"

urlpatterns = [
    path('game/add/', create_game, name='create_game'),
    path('game/delete/<int:game_id>/', delete_game, name='delete_game'),
    path('favorite_game/add/<int:game_id>/', add_favorite_game, name='add_favorite_game'),
    path('favorite_game/delete/<int:game_id>/', delete_favorite_game, name='delete_favorite_game')
]