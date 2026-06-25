from django.db import transaction

from .models import (
    Match,
    MatchPlayerScore,
)
from teams.models import TeamMembership
from .models import GameSession

from competitions.status_service import (
    TournamentStatusService,
)


class MatchScoringService:

    @staticmethod
    @transaction.atomic
    def finalize_match(match):
        
        if match.is_complete:
            return match

        team1_score = (
            MatchPlayerScore.objects.filter(
                match=match,
                team=match.team1
            ).values_list(
                'score',
                flat=True
            )
        )

        team2_score = (
            MatchPlayerScore.objects.filter(
                match=match,
                team=match.team2
            ).values_list(
                'score',
                flat=True
            )
        )

        score_team1 = sum(team1_score)
        score_team2 = sum(team2_score)

        match.score_team1 = score_team1
        match.score_team2 = score_team2

        match.save()

        TournamentStatusService.refresh_tournament(
            match.tournament
        )

        return match


    @staticmethod
    def can_finalize(match):

        team1_members = TeamMembership.objects.filter(
            team=match.team1
        ).count()

        team2_members = TeamMembership.objects.filter(
            team=match.team2
        ).count()

        team1_completed = GameSession.objects.filter(
            match=match,
            status='completed',
            user__teammembership__team=match.team1
        ).count()

        team2_completed = GameSession.objects.filter(
            match=match,
            status='completed',
            user__teammembership__team=match.team2
        ).count()

        return (
            team1_completed >= team1_members
            and
            team2_completed >= team2_members
        )