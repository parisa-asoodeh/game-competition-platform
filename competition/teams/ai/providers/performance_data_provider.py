from games.models import (
    Match,
    MatchPlayerScore,
)


class PerformanceDataProvider:

    @staticmethod
    def get_team_context(
        tournament,
        team,
    ):

        matches = list(

            Match.objects.filter(
                tournament=tournament,
            ).filter(
                team1=team,
            )

            |

            Match.objects.filter(
                tournament=tournament,
                team2=team,
            )

        )


        scores = list(

            MatchPlayerScore.objects.filter(
                match__in=matches,
                team=team,
            ).values_list(
                "score",
                flat=True,
            )

        )


        return {

            "team": team,

            "matches": matches,

            "scores": scores,

            "history": [],

            "mode": "current",
        }