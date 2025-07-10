from django.urls import path
from .views.views import create_game, delete_game

app_name = "bibliogames"

urlpatterns = [
    path('game/add/', create_game, name='create_game'),
    path('game/delete/<int:game_id>/', delete_game, name='delete_game')
]