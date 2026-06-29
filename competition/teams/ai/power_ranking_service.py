class PowerRankingService:


    @staticmethod
    def build(
        results,
    ):

        ranking = (
            PowerRankingService.build_initial_ranking(
                results,
            )
        )

        return ranking



    @staticmethod
    def build_initial_ranking(
        results,
    ):

        scores = {}


        for result in results:

            team1 = result["team1"]

            team2 = result["team2"]


            for team in (
                team1,
                team2,
            ):

                if team.id not in scores:

                    scores[team.id] = {

                        "team": team,

                        "score": 0,

                        "games": 0,
                    }



        for result in results:

            team1 = result["team1"]

            team2 = result["team2"]

            prediction = result["prediction"]

            winner = prediction["winner"]

            confidence = prediction["confidence"]


            scores[team1.id]["games"] += 1

            scores[team2.id]["games"] += 1



            if winner is None:

                continue



            if winner == team1:

                scores[team1.id]["score"] += confidence

                scores[team2.id]["score"] -= confidence



            elif winner == team2:

                scores[team2.id]["score"] += confidence

                scores[team1.id]["score"] -= confidence



        ranking = []


        for item in scores.values():

            games = item["games"]


            if games:

                power_score = (
                    item["score"]
                    /
                    games
                )

            else:

                power_score = 0



            ranking.append(

                {
                    "team": item["team"],

                    "score": round(
                        power_score,
                        1,
                    ),

                    "games": games,
                }

            )



        ranking.sort(

            key=lambda item: item["score"],

            reverse=True,

        )


        return ranking