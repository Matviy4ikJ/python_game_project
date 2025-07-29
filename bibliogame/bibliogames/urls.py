from django.urls import path
from .views.views import create_game, add_favorite_game, delete_favorite_game
from .views.moderation import moderation_list, moderate_game, delete_game, moderate_game_detail
from .views.game import index, game_detail
from .views.review import add_review, delete_review, edit_review

app_name = "bibliogames"

urlpatterns = [
    path('', index, name="index"),
    path('game/create/', create_game, name='create_game'),
    path('game/delete/<int:game_id>/', delete_game, name='delete_game'),
    path('favorite_game/add/<int:game_id>/', add_favorite_game, name='add_favorite_game'),
    path('favorite_game/delete/<int:game_id>/', delete_favorite_game, name='delete_favorite_game'),
    path('game/<int:pk>/', game_detail, name='game_detail'),
    path('game/moderate/<int:game_id>/<str:action>/', moderate_game, name="moderate_game"),
    path('game/moderate/<int:game_id>/', moderate_game_detail, name='moderate_game_detail'),
    path('game/moderate/list/', moderation_list, name="moderation_list"),
    path('games/<int:game_id>/review/', add_review, name='add_review'),
    path('reviews/<int:review_id>/delete/', delete_review, name='delete_review'),
    path('reviews/<int:review_id>/edit/', edit_review, name='edit_review'),
]
