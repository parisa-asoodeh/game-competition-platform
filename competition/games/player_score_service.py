from django.db.models import Sum

from .models import MatchPlayerScore
from teams.models import TeamMembership


class PlayerScoreService:

    @staticmethod
    def update_player_scores(match):

        player_scores = (
            MatchPlayerScore.objects
            .filter(match=match)
            .values(
                'user',
                'team'
            )
            .annotate(
                total=Sum('score')
            )
        )

        for item in player_scores:

            TeamMembership.objects.filter(
                user_id=item['user'],
                team_id=item['team']
            ).update(
                individual_score=item['total']
            )