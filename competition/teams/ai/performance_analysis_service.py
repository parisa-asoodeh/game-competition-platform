from .analyzers.score_analyzer import (
    ScoreAnalyzer,
)

from .analyzers.balance_analyzer import (
    BalanceAnalyzer,
)


class PerformanceAnalysisService:

    @staticmethod
    def generate(match):

        analyses = [

            ScoreAnalyzer.analyze(match),

            BalanceAnalyzer.analyze(match),

        ]

        return " ".join(analyses)