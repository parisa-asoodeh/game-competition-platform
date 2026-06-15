from django.contrib import admin
from .models import Team, TeamMembership


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'captain', 'total_score', 'created_at')
    search_fields = ('name', 'captain__username')
    list_filter = ('created_at',)


@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'individual_score')
    search_fields = ('user__username', 'team__name')