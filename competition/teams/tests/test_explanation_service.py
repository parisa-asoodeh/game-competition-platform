from django.test import SimpleTestCase

from teams.ai.explanation_service import (
    ExplanationService,
)


class ExplanationServiceTest(SimpleTestCase):

    def test_returns_counter_for_winner_reasons(self):

        winner = object()

        loser = object()

        votes = [

            {
                "vote": winner,
                "reason": "Reason A",
            },

            {
                "vote": winner,
                "reason": "Reason A",
            },

            {
                "vote": winner,
                "reason": "Reason B",
            },

            {
                "vote": loser,
                "reason": "Reason C",
            },
        ]

        result = (
            ExplanationService.build_prediction_reasons(
                votes,
                winner,
            )
        )

        self.assertEqual(
            result["Reason A"],
            2,
        )

        self.assertEqual(
            result["Reason B"],
            1,
        )

        self.assertNotIn(
            "Reason C",
            result,
        )


    def test_returns_empty_counter_when_no_vote_matches(self):

        winner = object()

        votes = [

            {
                "vote": object(),
                "reason": "Reason A",
            },

            {
                "vote": object(),
                "reason": "Reason B",
            },
        ]

        result = (
            ExplanationService.build_prediction_reasons(
                votes,
                winner,
            )
        )

        self.assertEqual(
            len(result),
            0,
        )


    def test_returns_empty_counter_for_empty_votes(self):

        result = (
            ExplanationService.build_prediction_reasons(
                [],
                object(),
            )
        )

        self.assertEqual(
            len(result),
            0,
        )