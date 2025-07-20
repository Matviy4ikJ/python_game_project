from django.urls import path
from .views.views import create_game, add_favorite_game, delete_favorite_game, game_detail
from .views.moderation import moderation_list, moderate_game, delete_game

app_name = "bibliogames"

urlpatterns = [
    path('game/create/', create_game, name='create_game'),
    path('game/delete/<int:game_id>/', delete_game, name='delete_game'),
    path('favorite_game/add/<int:game_id>/', add_favorite_game, name='add_favorite_game'),
    path('favorite_game/delete/<int:game_id>/', delete_favorite_game, name='delete_favorite_game'),
    path('game/<int:pk>/', game_detail, name='game_detail'),
    path('game/moderate/<int:game_id>/<str:action>/', moderate_game, name="moderate_game"),
    path('game/moderate/list/', moderation_list, name="moderation_list")
]