from django.test import TestCase

from accounts.models import CustomUser

from teams.models import Team

from teams.ai.power_ranking_service import (
    PowerRankingService,
)


class PowerRankingServiceTest(TestCase):

    def setUp(self):

        self.user1 = CustomUser.objects.create_user(
            username="u1",
            password="1234",
        )

        self.user2 = CustomUser.objects.create_user(
            username="u2",
            password="1234",
        )

        self.user3 = CustomUser.objects.create_user(
            username="u3",
            password="1234",
        )

        self.team1 = Team.objects.create(
            name="Alpha",
            captain=self.user1,
        )

        self.team2 = Team.objects.create(
            name="Beta",
            captain=self.user2,
        )

        self.team3 = Team.objects.create(
            name="Gamma",
            captain=self.user3,
        )


    def test_empty_results(self):

        result = PowerRankingService.build([])

        self.assertEqual(
            result,
            [],
        )


    def test_single_match(self):

        results = [

            {
                "team1": self.team1,
                "team2": self.team2,
                "prediction": {
                    "winner": self.team1,
                    "confidence": 80,
                },
            }
        ]

        ranking = PowerRankingService.build(
            results,
        )

        self.assertEqual(
            ranking[0]["team"],
            self.team1,
        )

        self.assertEqual(
            ranking[1]["team"],
            self.team2,
        )

        self.assertEqual(
            ranking[0]["power_rating"],
            100,
        )

        self.assertEqual(
            ranking[1]["power_rating"],
            0,
        )


    def test_draw_prediction(self):

        results = [

            {
                "team1": self.team1,
                "team2": self.team2,
                "prediction": {
                    "winner": None,
                    "confidence": 90,
                },
            }
        ]

        ranking = PowerRankingService.build(
            results,
        )

        self.assertEqual(
            ranking[0]["power_rating"],
            100,
        )

        self.assertEqual(
            ranking[1]["power_rating"],
            100,
        )


    def test_games_counter(self):

        results = [

            {
                "team1": self.team1,
                "team2": self.team2,
                "prediction": {
                    "winner": self.team1,
                    "confidence": 80,
                },
            },

            {
                "team1": self.team1,
                "team2": self.team3,
                "prediction": {
                    "winner": self.team3,
                    "confidence": 40,
                },
            },
        ]

        ranking = PowerRankingService.build(
            results,
        )

        games = {
            item["team"]: item["games"]
            for item in ranking
        }

        self.assertEqual(
            games[self.team1],
            2,
        )

        self.assertEqual(
            games[self.team2],
            1,
        )

        self.assertEqual(
            games[self.team3],
            1,
        )


    def test_scores_are_sorted_descending(self):

        results = [

            {
                "team1": self.team1,
                "team2": self.team2,
                "prediction": {
                    "winner": self.team1,
                    "confidence": 80,
                },
            },

            {
                "team1": self.team1,
                "team2": self.team3,
                "prediction": {
                    "winner": self.team3,
                    "confidence": 40,
                },
            },
        ]

        ranking = PowerRankingService.build(
            results,
        )

        scores = [
            item["score"]
            for item in ranking
        ]

        self.assertEqual(
            scores,
            sorted(
                scores,
                reverse=True,
            ),
        )


    def test_normalize_equal_scores(self):

        ranking = [

            {
                "team": self.team1,
                "score": 0,
            },

            {
                "team": self.team2,
                "score": 0,
            },
        ]

        ranking = (
            PowerRankingService.normalize(
                ranking
            )
        )

        self.assertEqual(
            ranking[0]["power_rating"],
            100,
        )

        self.assertEqual(
            ranking[1]["power_rating"],
            100,
        )


    def test_normalize_range(self):

        ranking = [

            {
                "team": self.team1,
                "score": 20,
            },

            {
                "team": self.team2,
                "score": 10,
            },

            {
                "team": self.team3,
                "score": 0,
            },
        ]

        ranking = (
            PowerRankingService.normalize(
                ranking
            )
        )

        self.assertEqual(
            ranking[0]["power_rating"],
            100,
        )

        self.assertEqual(
            ranking[1]["power_rating"],
            50,
        )

        self.assertEqual(
            ranking[2]["power_rating"],
            0,
        )