from django.contrib import admin
from .models import Game, Developer, Genre, Platforms, Review, Favorites, FavoriteGame


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'developer', 'status')
    list_filter = ('status', 'genres', 'platforms')
    search_fields = ('title', 'description')


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Platforms)
class PlatformsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'rating', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('user__username', 'game__title')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = 'Approve selected reviews'


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')


@admin.register(FavoriteGame)
class FavoriteGameAdmin(admin.ModelAdmin):
    list_display = ('favorites', 'game')
    search_fields = ('game__title',)
