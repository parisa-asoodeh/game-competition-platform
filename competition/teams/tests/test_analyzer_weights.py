from django.test import SimpleTestCase

from teams.ai.analyzer_weights import (
    ANALYZER_WEIGHTS,
)


class AnalyzerWeightsTest(SimpleTestCase):

    def test_contains_all_analyzers(self):

        expected = {
            "AverageVote",
            "MomentumVote",
            "ConsistencyVote",
            "MatchDifficultyVote",
            "StarDependencyVote",
        }

        self.assertEqual(
            set(ANALYZER_WEIGHTS.keys()),
            expected,
        )


    def test_weights_are_positive_numbers(self):

        for weight in ANALYZER_WEIGHTS.values():

            self.assertIsInstance(
                weight,
                (int, float),
            )

            self.assertGreater(
                weight,
                0,
            )