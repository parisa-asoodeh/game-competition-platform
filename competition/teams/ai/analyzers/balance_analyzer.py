from games.models import MatchPlayerScore


class BalanceAnalyzer:

    @staticmethod
    def analyze(match):

        team1_scores = list(
            MatchPlayerScore.objects.filter(
                match=match,
                team=match.team1
            ).values_list(
                "score",
                flat=True
            )
        )

        team2_scores = list(
            MatchPlayerScore.objects.filter(
                match=match,
                team=match.team2
            ).values_list(
                "score",
                flat=True
            )
        )

        team1_balanced = (
            BalanceAnalyzer.is_balanced(
                team1_scores
            )
        )

        team2_balanced = (
            BalanceAnalyzer.is_balanced(
                team2_scores
            )
        )

        if team1_balanced and team2_balanced:

            return (
                "هر دو تیم عملکردی هماهنگ و گروهی داشتند."
            )

        if team1_balanced:

            return (
                f"{match.team1.name} "
                f"عملکرد گروهی‌تری داشت."
            )

        if team2_balanced:

            return (
                f"{match.team2.name} "
                f"عملکرد گروهی‌تری داشت."
            )

        return (
            "هر دو تیم بیش از حد به عملکرد چند بازیکن متکی بودند."
        )

    @staticmethod
    def is_balanced(scores):

        if len(scores) < 2:
            return True

        return (
            max(scores) - min(scores)
        ) <= 20