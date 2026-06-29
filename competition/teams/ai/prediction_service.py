from teams.ai.predictors.winner_predictor import (
    WinnerPredictor,
)
from teams.ai.predictors.champion_predictor import (
    ChampionPredictor,
)


class PredictionService:

    @staticmethod
    def predict_match(
        team1,
        team2,
    ):

        return WinnerPredictor.predict(
            team1,
            team2,
        )

    @staticmethod
    def predict_league():

        pass


    @staticmethod
    def predict_champion(
        tournament,
    ):

        teams = [

            tournament_team.team

            for tournament_team in tournament.teams.all()

        ]

        return ChampionPredictor.predict(
            teams=teams,
        )


    @staticmethod
    def simulate_match():

        pass