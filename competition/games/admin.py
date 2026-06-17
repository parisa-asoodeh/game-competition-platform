from django.contrib import admin
from .models import Match

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'tournament',
        'team1',
        'score_team1',
        'team2',
        'score_team2',
        'winner',
        'played_at'
    )
    list_filter = (
        'tournament',
        'played_at',
    )