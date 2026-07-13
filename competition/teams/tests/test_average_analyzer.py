from django.test import TestCase

from accounts.models import CustomUser
from teams.models import Team

from teams.ai.analyzers.average_analyzer import (
    AverageAnalyzer,
)

class AverageAnalyzerTest(TestCase):
    def setUp(self):

        self.user = CustomUser.objects.create_user(
            username="user1",
            password="1234",
        )

        self.team = Team.objects.create(
            name="Alpha",
            captain=self.user,
        )


    def test_average_with_empty_scores(
        self,
    ):

        # Act
        result = AverageAnalyzer.average([])

        # Assert
        self.assertEqual(
            result["total"],
            0,
        )

        self.assertEqual(
            result["players"],
            0,
        )

        self.assertEqual(
            result["average"],
            0,
        )

    def test_average_with_scores(
        self,
    ):

        # Act
        result = AverageAnalyzer.average(
            [10, 20, 30],
        )

        # Assert
        self.assertEqual(
            result["total"],
            60,
        )

        self.assertEqual(
            result["players"],
            3,
        )

        self.assertEqual(
            result["average"],
            20,
        )

    def test_build_summary(
        self,
    ):

        # Arrange
        result = {
            "average": 15.5,
            "total": 31,
            "players": 2,
        }

        # Act
        summary = AverageAnalyzer.build_summary(
            self.team,
            result,
        )

        # Assert
        self.assertEqual(
            summary,
            "میانگین امتیاز اعضای Alpha (15.5) است.",
        )

    def test_analyze(
        self,
    ):

        # Arrange
        team_context = {
            "team": self.team,
            "scores": [10, 20, 30],
            "history": [],
            "matches": [],
            "mode": "current",
        }

        # Act
        result = AverageAnalyzer.analyze(
            team_context,
        )

        # Assert
        self.assertEqual(
            result["total"],
            60,
        )

        self.assertEqual(
            result["players"],
            3,
        )

        self.assertEqual(
            result["average"],
            20,
        )

        self.assertEqual(
            result["summary"],
            "میانگین امتیاز اعضای Alpha (20.0) است.",
        )