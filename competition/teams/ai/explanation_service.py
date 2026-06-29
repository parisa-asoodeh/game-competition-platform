from collections import Counter


class ExplanationService:

    @staticmethod
    def build_prediction_reasons(
        votes,
        winner,
    ):

        reasons = []

        for vote in votes:

            if vote["vote"] != winner:
                continue

            reasons.append(
                vote["reason"]
            )

        return Counter(reasons)