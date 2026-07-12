from django.test import TestCase
from django.contrib.auth import get_user_model

from teams.models import (
    Team,
    TeamMembership,
)

from competitions.models import (
    Tournament,
    TournamentTeam,
    GameType,
)

from games.models import (
    Match,
    GameSession,
    MatchPlayerScore,
)

from games.match_scoring_service import (
    MatchScoringService,
)

from unittest.mock import patch

User = get_user_model()


class MatchScoringServiceTest(TestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(
            username="user1",
            password="1234",
        )

        self.user2 = User.objects.create_user(
            username="user2",
            password="1234",
        )

        self.team1 = Team.objects.create(
            name="Team 1",
            captain=self.user1,
        )

        self.team2 = Team.objects.create(
            name="Team 2",
            captain=self.user2,
        )

        TeamMembership.objects.create(
            team=self.team1,
            user=self.user1,
        )

        TeamMembership.objects.create(
            team=self.team2,
            user=self.user2,
        )

        self.game_type = GameType.objects.create(
            name="Quiz",
            key="quiz",
        )

        self.tournament = Tournament.objects.create(
            name="League",
            game_type=self.game_type,
        )

        TournamentTeam.objects.create(
            tournament=self.tournament,
            team=self.team1,
        )

        TournamentTeam.objects.create(
            tournament=self.tournament,
            team=self.team2,
        )

        self.match = Match.objects.create(
            tournament=self.tournament,
            team1=self.team1,
            team2=self.team2,
        )


    def test_can_finalize_when_all_players_completed(self):

        GameSession.objects.create(
            match=self.match,
            user=self.user1,
            status="completed",
        )

        GameSession.objects.create(
            match=self.match,
            user=self.user2,
            status="completed",
        )

        self.assertTrue(
            MatchScoringService.can_finalize(
                self.match
            )
        )


    def test_can_not_finalize_when_some_players_not_completed(self):

        GameSession.objects.create(
            match=self.match,
            user=self.user1,
            status="completed",
        )

        GameSession.objects.create(
            match=self.match,
            user=self.user2,
            status="pending",
        )

        self.assertFalse(
            MatchScoringService.can_finalize(
                self.match
            )
        )


    @patch(
        "games.match_scoring_service.TournamentStatusService.refresh_tournament"
    )
    def test_finalize_match_updates_team_scores(
        self,
        mock_refresh,
    ):

        # Arrange
        MatchPlayerScore.objects.create(
            match=self.match,
            user=self.user1,
            team=self.team1,
            score=15,
        )

        MatchPlayerScore.objects.create(
            match=self.match,
            user=self.user2,
            team=self.team2,
            score=10,
        )

        # Act
        MatchScoringService.finalize_match(
            self.match
        )

        self.match.refresh_from_db()

        # Assert
        self.assertEqual(
            self.match.score_team1,
            15,
        )

        self.assertEqual(
            self.match.score_team2,
            10,
        )

        mock_refresh.assert_called_with(
            self.tournament
        )


    @patch(
        "games.match_scoring_service.TournamentStatusService.refresh_tournament"
    )
    def test_finalize_match_sets_team1_as_winner(
        self,
        mock_refresh,
    ):

        # Arrange
        MatchPlayerScore.objects.create(
            match=self.match,
            user=self.user1,
            team=self.team1,
            score=20,
        )

        MatchPlayerScore.objects.create(
            match=self.match,
            user=self.user2,
            team=self.team2,
            score=10,
        )

        # Act
        MatchScoringService.finalize_match(
            self.match
        )

        self.match.refresh_from_db()

        # Assert
        self.assertEqual(
            self.match.winner,
            self.team1,
        )

        mock_refresh.assert_called_with(
            self.tournament
        )


    @patch(
        "games.match_scoring_service.TournamentStatusService.refresh_tournament"
    )
    def test_finalize_match_sets_team2_as_winner(
        self,
        mock_refresh,
    ):

        # Arrange
        MatchPlayerScore.objects.create(
            match=self.match,
            user=self.user1,
            team=self.team1,
            score=10,
        )

        MatchPlayerScore.objects.create(
            match=self.match,
            user=self.user2,
            team=self.team2,
            score=20,
        )

        # Act
        MatchScoringService.finalize_match(
            self.match
        )

        self.match.refresh_from_db()

        # Assert
        self.assertEqual(
            self.match.score_team1,
            10,
        )

        self.assertEqual(
            self.match.score_team2,
            20,
        )

        self.assertEqual(
            self.match.winner,
            self.team2,
        )

        mock_refresh.assert_called_with(
            self.tournament
        )


    @patch(
        "games.match_scoring_service.TournamentStatusService.refresh_tournament"
    )
    def test_finalize_match_sets_draw(
        self,
        mock_refresh,
    ):

        # Arrange
        MatchPlayerScore.objects.create(
            match=self.match,
            user=self.user1,
            team=self.team1,
            score=15,
        )

        MatchPlayerScore.objects.create(
            match=self.match,
            user=self.user2,
            team=self.team2,
            score=15,
        )

        # Act
        MatchScoringService.finalize_match(
            self.match
        )

        self.match.refresh_from_db()

        # Assert
        self.assertEqual(
            self.match.score_team1,
            15,
        )

        self.assertEqual(
            self.match.score_team2,
            15,
        )

        self.assertIsNone(
            self.match.winner,
        )

        mock_refresh.assert_called_with(
            self.tournament
        )


    @patch(
        "games.match_scoring_service.TournamentStatusService.refresh_tournament"
    )
    def test_finalize_match_when_match_is_already_complete(
        self,
        mock_refresh,
    ):

        # Arrange
        self.match.score_team1 = 15
        self.match.score_team2 = 10
        self.match.save()

        # Act
        result = MatchScoringService.finalize_match(
            self.match
        )

        self.match.refresh_from_db()

        # Assert
        self.assertEqual(
            result,
            self.match,
        )

        self.assertEqual(
            self.match.score_team1,
            15,
        )

        self.assertEqual(
            self.match.score_team2,
            10,
        )

        mock_refresh.assert_not_called()