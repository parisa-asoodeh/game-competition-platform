from teams.ai.votes.average_vote import (
    AverageVote,
)

from teams.ai.votes.momentum_vote import (
    MomentumVote,
)

from teams.ai.votes.consistency_vote import (
    ConsistencyVote,
)

from teams.ai.votes.match_difficulty_vote import (
    MatchDifficultyVote,
)

from teams.ai.votes.star_dependency_vote import (
    StarDependencyVote,
)
from teams.ai.analyzer_weights import (
    ANALYZER_WEIGHTS,
)
from teams.ai.providers.performance_data_provider import (
    PerformanceDataProvider,
)


class WinnerPredictor:

    VOTES = [

        AverageVote,

        MomentumVote,

        ConsistencyVote,

        MatchDifficultyVote,

        StarDependencyVote,
    ]

    @staticmethod
    def predict(
        team1,
        team2,
        tournament,
    ):

        team1_context = (
            PerformanceDataProvider.get_team_context(
                tournament,
                team1,
            )
        )

        team2_context = (
            PerformanceDataProvider.get_team_context(
                tournament,
                team2,
            )
        )

        votes = WinnerPredictor.collect_votes(
            team1_context,
            team2_context,
        )

        scores = WinnerPredictor.calculate_scores(
            votes,
            team1,
            team2,
        )

        winner = WinnerPredictor.choose_winner(
            scores,
            team1,
            team2,
        )

        confidence = (
            WinnerPredictor.calculate_confidence(
                scores,
                winner,
                team1,
                team2,
            )
        )

        summary = WinnerPredictor.build_summary(
            winner,
            confidence,
        )

        return {

            "winner": winner,

            "confidence": confidence,

            "votes": votes,

            "vote_scores": scores,

            "prediction_summary": summary,

            "team1_context": team1_context,

            "team2_context": team2_context,
        }
        


    @staticmethod
    def collect_votes(
        team1_context,
        team2_context,
    ):

        votes = []

        for vote_class in WinnerPredictor.VOTES:

            result = vote_class.vote(
                team1_context,
                team2_context,
            )

            votes.append(
                result
            )

        return votes
    


    @staticmethod
    def calculate_scores(
        votes,
        team1,
        team2,
    ):

        scores = {

            team1.id: 0,

            team2.id: 0,
        }

        for vote in votes:

            weight = ANALYZER_WEIGHTS.get(
                vote["analyzer"],
                1,
            )

            weighted_confidence = (
                vote["confidence"] * weight
            )

            if vote["vote"] == team1:

                scores[team1.id] += (
                    weighted_confidence
                )

            elif vote["vote"] == team2:

                scores[team2.id] += (
                    weighted_confidence
                )

        return scores


    @staticmethod
    def choose_winner(
        scores,
        team1,
        team2,
    ):

        team1_score = scores[team1.id]
        team2_score = scores[team2.id]

        if team1_score > team2_score:
            return team1

        if team2_score > team1_score:
            return team2

        return None   


    @staticmethod
    def calculate_confidence(
        scores,
        winner,
        team1,
        team2,
    ):

        total = (
            scores[team1.id]
            +
            scores[team2.id]
        )

        if total == 0:

            return 0

        if winner == team1:

            confidence = (
                scores[team1.id]
                /
                total
            ) * 100

        elif winner == team2:

            confidence = (
                scores[team2.id]
                /
                total
            ) * 100

        else:

            return 0

        return round(
            confidence,
            1
        )

    @staticmethod
    def build_summary(
        winner,
        confidence,
    ):

        if winner is None:

            return (
                "هوش مصنوعی برنده مشخصی را "
                "پیش‌بینی نمی‌کند."
            )

        return (
            f"هوش مصنوعی شانس پیروزی "
            f"{winner.name} "
            f"را "
            f"{confidence:.1f}٪ "
            f"ارزیابی می‌کند."
        )