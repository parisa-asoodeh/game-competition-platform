from unittest.mock import patch

from django.test import TestCase

from accounts.models import CustomUser

from teams.models import Team

from teams.ai.analyzers.momentum_analyzer import (
    MomentumAnalyzer,
)

class MomentumAnalyzerTest(TestCase):
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
        "teams.ai.analyzers.momentum_analyzer.TeamAnalysisService.get_recent_scores_from_context"
    )
    def test_analyze_without_scores(
        self,
        mock_scores,
    ):

        mock_scores.return_value = []

        result = MomentumAnalyzer.analyze(
            self.team_context,
        )

        self.assertEqual(
            result["scores"],
            [],
        )

        self.assertEqual(
            result["change"],
            0,
        )

        self.assertEqual(
            result["trend"],
            "stable",
        )

        self.assertEqual(
            result["summary"],
            "داده کافی برای تحلیل روند وجود ندارد.",
        )


    @patch(
        "teams.ai.analyzers.momentum_analyzer.TeamAnalysisService.get_recent_scores_from_context"
    )
    def test_analyze_with_up_trend(
        self,
        mock_scores,
    ):

        mock_scores.return_value = [30, 40, 50]

        result = MomentumAnalyzer.analyze(
            self.team_context,
        )

        self.assertEqual(
            result["change"],
            20,
        )

        self.assertEqual(
            result["trend"],
            "up",
        )

        self.assertEqual(
            result["summary"],
            "روند عملکرد Alpha در مسابقات اخیر صعودی بوده است.",
        )


    @patch(
        "teams.ai.analyzers.momentum_analyzer.TeamAnalysisService.get_recent_scores_from_context"
    )
    def test_analyze_with_down_trend(
        self,
        mock_scores,
    ):

        mock_scores.return_value = [60, 45, 40]

        result = MomentumAnalyzer.analyze(
            self.team_context,
        )

        self.assertEqual(
            result["change"],
            -20,
        )

        self.assertEqual(
            result["trend"],
            "down",
        )

        self.assertEqual(
            result["summary"],
            "روند عملکرد Alpha در مسابقات اخیر نزولی بوده است.",
        )

    @patch(
        "teams.ai.analyzers.momentum_analyzer.TeamAnalysisService.get_recent_scores_from_context"
    )
    def test_analyze_with_stable_trend(
        self,
        mock_scores,
    ):

        mock_scores.return_value = [40, 45, 50]

        result = MomentumAnalyzer.analyze(
            self.team_context,
        )

        self.assertEqual(
            result["change"],
            10,
        )

        self.assertEqual(
            result["trend"],
            "stable",
        )

        self.assertEqual(
            result["summary"],
            "عملکرد Alpha در مسابقات اخیر تقریباً ثابت بوده است.",
        )

    def test_build_summary_with_up_trend(
        self,
    ):

        result = MomentumAnalyzer.build_summary(
            self.team,
            "up",
            20,
        )

        self.assertEqual(
            result,
            "روند عملکرد Alpha در مسابقات اخیر صعودی بوده است.",
        )

    def test_build_summary_with_stable_trend(
        self,
    ):

        result = MomentumAnalyzer.build_summary(
            self.team,
            "stable",
            0,
        )

        self.assertEqual(
            result,
            "عملکرد Alpha در مسابقات اخیر تقریباً ثابت بوده است.",
        )