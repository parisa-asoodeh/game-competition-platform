from teams.ai.analyzers.momentum_analyzer import (
    MomentumAnalyzer,
)


class MomentumVote:

    @staticmethod
    def vote(
        team1,
        team2,
    ):

        team1_result = (
            MomentumAnalyzer.analyze(
                team1
            )
        )

        team2_result = (
            MomentumAnalyzer.analyze(
                team2
            )
        )

        team1_trend = (
            team1_result["trend"]
        )

        team2_trend = (
            team2_result["trend"]
        )

        if team1_trend == team2_trend:

            vote = None

        elif team1_trend == "up":

            vote = team1

        elif team2_trend == "up":

            vote = team2

        elif team1_trend == "stable":

            vote = team1

        else:

            vote = team2

        confidence = abs(
            team1_result["change"] -
            team2_result["change"]
        )

        if vote == team1:

            reason = (
                f"روند عملکرد "
                f"{team1.name} "
                f"بهتر است."
            )

        elif vote == team2:

            reason = (
                f"روند عملکرد "
                f"{team2.name} "
                f"بهتر است."
            )

        else:

            reason = (
                "روند عملکرد دو تیم مشابه است."
            )

        return {

            "analyzer": "MomentumVote",

            "vote": vote,

            "confidence": confidence,

            "reason": reason,
        }