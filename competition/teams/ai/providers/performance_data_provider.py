from games.models import Match


class PerformanceDataProvider:

    @staticmethod
    def get_team_context(
        tournament,
        team,
    ):

        matches = Match.objects.filter(
            tournament=tournament,
        ).filter(
            team1=team,
        ) | Match.objects.filter(
            tournament=tournament,
            team2=team,
        )

        return {

            "team": team,

            "matches": list(matches),

            "history": [],

            "mode": "current",
        }