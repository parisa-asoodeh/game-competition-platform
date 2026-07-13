from unittest.mock import patch

from django.test import TestCase

from accounts.models import CustomUser

from teams.models import Team

from teams.ai.analyzers.match_difficulty_analyzer import (
    MatchDifficultyAnalyzer,
)

class MatchDifficultyAnalyzerTest(TestCase):
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
        "teams.ai.analyzers.match_difficulty_analyzer.TeamAnalysisService.get_recent_score_differences_from_context"
    )
    def test_analyze_without_data(
        self,
        mock_differences,
    ):

        mock_differences.return_value = []

        result = MatchDifficultyAnalyzer.analyze(
            self.team_context,
        )

        self.assertEqual(
            result["difficulty"],
            "unknown",
        )

        self.assertEqual(
            result["average_difference"],
            0,
        )

        self.assertEqual(
            result["summary"],
            "داده کافی برای تحلیل سختی مسابقات وجود ندارد.",
        )

    @patch(
        "teams.ai.analyzers.match_difficulty_analyzer.TeamAnalysisService.get_recent_score_differences_from_context"
    )
    def test_analyze_with_hard_difficulty(
        self,
        mock_differences,
    ):

        mock_differences.return_value = [5, 10, 8]

        result = MatchDifficultyAnalyzer.analyze(
            self.team_context,
        )

        self.assertEqual(
            result["difficulty"],
            "hard",
        )

        self.assertEqual(
            result["average_difference"],
            7.7,
        )

        self.assertEqual(
            result["summary"],
            "مسابقات اخیر Alpha بسیار رقابتی بوده‌اند.",
        )

    @patch(
        "teams.ai.analyzers.match_difficulty_analyzer.TeamAnalysisService.get_recent_score_differences_from_context"
    )
    def test_analyze_with_medium_difficulty(
        self,
        mock_differences,
    ):

        mock_differences.return_value = [20, 25, 30]

        result = MatchDifficultyAnalyzer.analyze(
            self.team_context,
        )

        self.assertEqual(
            result["difficulty"],
            "medium",
        )

        self.assertEqual(
            result["average_difference"],
            25.0,
        )

        self.assertEqual(
            result["summary"],
            "مسابقات اخیر Alpha از نظر سختی در سطح متوسط بوده‌اند.",
        )

    @patch(
        "teams.ai.analyzers.match_difficulty_analyzer.TeamAnalysisService.get_recent_score_differences_from_context"
    )
    def test_analyze_with_easy_difficulty(
        self,
        mock_differences,
    ):

        mock_differences.return_value = [40, 45, 50]

        result = MatchDifficultyAnalyzer.analyze(
            self.team_context,
        )

        self.assertEqual(
            result["difficulty"],
            "easy",
        )

        self.assertEqual(
            result["average_difference"],
            45.0,
        )

        self.assertEqual(
            result["summary"],
            "مسابقات اخیر Alpha نسبتاً آسان بوده‌اند.",
        )

    def test_build_summary_with_hard_difficulty(
        self,
    ):

        result = MatchDifficultyAnalyzer.build_summary(
            self.team,
            "hard",
        )

        self.assertEqual(
            result,
            "مسابقات اخیر Alpha بسیار رقابتی بوده‌اند.",
        )

    def test_build_summary_with_easy_difficulty(
        self,
    ):

        result = MatchDifficultyAnalyzer.build_summary(
            self.team,
            "easy",
        )

        self.assertEqual(
            result,
            "مسابقات اخیر Alpha نسبتاً آسان بوده‌اند.",
        )