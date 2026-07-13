from django.test import TestCase

from accounts.models import CustomUser

from teams.models import Team

from teams.ai.analyzers.star_dependency_analyzer import (
    StarDependencyAnalyzer,
)

class StarDependencyAnalyzerTest(TestCase):
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
            "scores": [],
        }

    def test_dependency_percentage_without_scores(
        self,
    ):

        result = (
            StarDependencyAnalyzer.dependency_percentage(
                [],
            )
        )

        self.assertEqual(
            result,
            {
                "total": 0,
                "top_score": 0,
                "percentage": 0,
            },
        )


    def test_dependency_percentage(
        self,
    ):

        result = (
            StarDependencyAnalyzer.dependency_percentage(
                [20, 30, 50],
            )
        )

        self.assertEqual(
            result["total"],
            100,
        )

        self.assertEqual(
            result["top_score"],
            50,
        )

        self.assertEqual(
            result["percentage"],
            50,
        )

    def test_build_summary_with_low_dependency(
        self,
    ):

        result = StarDependencyAnalyzer.build_summary(
            self.team,
            {
                "percentage": 35,
            },
        )

        self.assertEqual(
            result,
            "امتیازگیری اعضای تیم Alpha متعادل بوده و وابستگی زیادی به یک بازیکن وجود ندارد.",
        )

    def test_build_summary_with_medium_dependency(
        self,
    ):

        result = StarDependencyAnalyzer.build_summary(
            self.team,
            {
                "percentage": 50,
            },
        )

        self.assertEqual(
            result,
            "بهترین بازیکن تیم Alpha 50٪ از امتیازات تیم را کسب کرده است.",
        )

    def test_build_summary_with_high_dependency(
        self,
    ):

        result = StarDependencyAnalyzer.build_summary(
            self.team,
            {
                "percentage": 75,
            },
        )

        self.assertEqual(
            result,
            "بیش از 75٪ از امتیازات تیم Alpha توسط یک بازیکن کسب شده و تیم وابستگی زیادی به او دارد.",
        )

    def test_analyze_without_scores(
        self,
    ):

        result = StarDependencyAnalyzer.analyze(
            self.team_context,
        )

        self.assertEqual(
            result["total"],
            0,
        )

        self.assertEqual(
            result["top_score"],
            0,
        )

        self.assertEqual(
            result["percentage"],
            0,
        )

        self.assertEqual(
            result["summary"],
            "امتیازگیری اعضای تیم Alpha متعادل بوده و وابستگی زیادی به یک بازیکن وجود ندارد.",
        )


    def test_analyze(
        self,
    ):

        self.team_context["scores"] = [
            20,
            30,
            50,
        ]

        result = StarDependencyAnalyzer.analyze(
            self.team_context,
        )

        self.assertEqual(
            result["total"],
            100,
        )

        self.assertEqual(
            result["top_score"],
            50,
        )

        self.assertEqual(
            result["percentage"],
            50,
        )

        self.assertEqual(
            result["summary"],
            "بهترین بازیکن تیم Alpha 50٪ از امتیازات تیم را کسب کرده است.",
        )