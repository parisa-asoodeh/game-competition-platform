from django.shortcuts import render, get_object_or_404

from .models import Tournament


def tournament_leaderboard(request, tournament_id):

    tournament = get_object_or_404(
        Tournament,
        id=tournament_id
    )

    teams = [
        tt.team
        for tt in tournament.teams.select_related(
            'team'
        )
    ]

    table = []

    for team in teams:

        table.append({
            'team': team,
            'points': team.get_points_in_tournament(
                tournament
            ),
            'wins': team.get_wins_in_tournament(
                tournament
            ),
            'draws': team.get_draws_in_tournament(
                tournament
            ),
            'losses': team.get_losses_in_tournament(
                tournament
            ),
        })

    table.sort(
        key=lambda row: row['points'],
        reverse=True
    )

    return render(
        request,
        'competitions/tournament_leaderboard.html',
        {
            'tournament': tournament,
            'table': table,
        }
    )