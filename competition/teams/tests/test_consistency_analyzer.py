from unittest.mock import patch

from django.test import TestCase

from accounts.models import CustomUser

from teams.models import Team

from teams.ai.analyzers.consistency_analyzer import (
    ConsistencyAnalyzer,
)

class ConsistencyAnalyzerTest(TestCase):
    def setUp(self):

        self.user = CustomUser.objects.create_user(
            username="user1",
            password="1234",
        )

        self.team = Team.objects.create(
            name="Alpha",
            captain=self.user,
        )

        self.team_context = {
            "team": self.team,
        }

    @patch(
        "teams.ai.analyzers.consistency_analyzer.TeamAnalysisService.get_recent_scores_from_context"
    )
    def test_analyze_without_scores(
        self,
        mock_scores,
    ):

        mock_scores.return_value = []

        result = ConsistencyAnalyzer.analyze(
            self.team_context,
        )

        self.assertEqual(
            result["scores"],
            [],
        )

        self.assertEqual(
            result["variation"],
            0,
        )

        self.assertEqual(
            result["consistency"],
            "unknown",
        )

        self.assertEqual(
            result["summary"],
            "داده کافی برای تحلیل ثبات عملکرد وجود ندارد.",
        )


    @patch(
        "teams.ai.analyzers.consistency_analyzer.TeamAnalysisService.get_recent_scores_from_context"
    )
    def test_analyze_with_high_consistency(
        self,
        mock_scores,
    ):

        mock_scores.return_value = [50, 55, 60]

        result = ConsistencyAnalyzer.analyze(
            self.team_context,
        )

        self.assertEqual(
            result["variation"],
            10,
        )

        self.assertEqual(
            result["consistency"],
            "high",
        )

        self.assertEqual(
            result["summary"],
            "عملکرد Alpha در مسابقات اخیر بسیار باثبات بوده است.",
        )


    @patch(
        "teams.ai.analyzers.consistency_analyzer.TeamAnalysisService.get_recent_scores_from_context"
    )
    def test_analyze_with_medium_consistency(
        self,
        mock_scores,
    ):

        mock_scores.return_value = [40, 55, 70]

        result = ConsistencyAnalyzer.analyze(
            self.team_context,
        )

        self.assertEqual(
            result["variation"],
            30,
        )

        self.assertEqual(
            result["consistency"],
            "medium",
        )

        self.assertEqual(
            result["summary"],
            "عملکرد Alpha در مسابقات اخیر ثبات قابل قبولی داشته است.",
        )


    @patch(
        "teams.ai.analyzers.consistency_analyzer.TeamAnalysisService.get_recent_scores_from_context"
    )
    def test_analyze_with_low_consistency(
        self,
        mock_scores,
    ):

        mock_scores.return_value = [20, 60, 80]

        result = ConsistencyAnalyzer.analyze(
            self.team_context,
        )

        self.assertEqual(
            result["variation"],
            60,
        )

        self.assertEqual(
            result["consistency"],
            "low",
        )

        self.assertEqual(
            result["summary"],
            "عملکرد Alpha در مسابقات اخیر نوسان زیادی داشته است.",
        )


    def test_build_summary_with_high_consistency(
        self,
    ):

        result = ConsistencyAnalyzer.build_summary(
            self.team,
            "high",
        )

        self.assertEqual(
            result,
            "عملکرد Alpha در مسابقات اخیر بسیار باثبات بوده است.",
        )


    def test_build_summary_with_low_consistency(
        self,
    ):

        result = ConsistencyAnalyzer.build_summary(
            self.team,
            "low",
        )

        self.assertEqual(
            result,
            "عملکرد Alpha در مسابقات اخیر نوسان زیادی داشته است.",
        )