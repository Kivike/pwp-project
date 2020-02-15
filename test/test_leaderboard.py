import unittest
from sqlalchemy import exc

from src.app import create_app, db
from src.orm_models import Leaderboard, GameType, Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # is_valid, wins, losses
    win_loss_cases = [
        (True, 0, 0),
        (True, 5, 1),
        (False, None, 0),
        (False, None, 5),
        (False, 0, None),
        (False, 3, None)
    ]

    def testCreateAndDeleteLeaderboardEntry(self):
        leaderboard = Leaderboard(
            game_type = self.create_game_type(),
            player = self.create_player(),
            wins = 0,
            losses = 0
        )

        db.session.add(leaderboard)
        db.session.commit()

        assert Leaderboard.query.count() == 1

        db.session.delete(leaderboard)
        db.session.commit()

        assert Leaderboard.query.count() == 0

    def testLeaderboardWinsAndLosses(self):
        leaderboard = Leaderboard(
            game_type = self.create_game_type(),
            player = self.create_player()
        )
        for is_valid, wins, losses in self.win_loss_cases:
            leaderboard.wins = wins
            leaderboard.losses = losses

            db.session.add(leaderboard)

            if is_valid == True:
                db.session.commit()
                assert Leaderboard.query.count() == 1
            else:
                with self.assertRaises(exc.IntegrityError):
                    db.session.commit()
                
                db.session.rollback()

    def testDuplicateEntryThrowsError(self):
        game_type = self.create_game_type()
        player = self.create_player()

        leaderboard_1 = Leaderboard(game_type = game_type)
        leaderboard_2 = Leaderboard(player = player)

        db.session.add(leaderboard_1)
        db.session.add(leaderboard_2)

        with self.assertRaises(exc.IntegrityError):
            db.session.commit()

    def create_game_type(self):
        game_type = GameType(name="chess", max_players=3)
        db.session.add(game_type)
        db.session.commit()
        return game_type
    
    def create_player(self):
        player = Player(name="Alice")
        db.session.add(player)
        db.session.commit()
        return player