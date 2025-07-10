from django.contrib import admin
from bibliogames.models import Game, Developer, Genre, Platforms


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