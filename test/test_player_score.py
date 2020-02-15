import unittest
from sqlalchemy import exc

from src.app import create_app, db
from src.orm_models import Player, PlayerScore, GameType, Game

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

    def testCreateAndDeleteValidPlayer(self):
        player = self.create_player()
        game = self.create_basic_game()
        player_score = PlayerScore(game=game, player=player)

        db.session.add(player_score)
        db.session.commit()

        assert PlayerScore.query.count() == 1

        db.session.delete(player_score)
        db.session.commit()

        assert PlayerScore.query.count() == 0

    def testCreatePlayerScoreWithoutPlayerThrowsError(self):
        game = self.create_basic_game()
        player_score = PlayerScore(game=game)

        db.session.add(player_score)

        with self.assertRaises(exc.IntegrityError):
            db.session.commit()

    def testCreatePlayerScoreWithoutGameThrowsError(self):
        player = self.create_player()
        player_score = PlayerScore(player=player)

        db.session.add(player_score)

        with self.assertRaises(exc.IntegrityError):
            db.session.commit()

    def create_basic_game(self):
        game_type = GameType(name="chess", max_players=3)
        host = Player(name="Test player")
        game = Game(game_type=game_type, host=host, game_token="test")

        db.session.add(game_type)
        db.session.add(host)
        db.session.add(game)
        db.session.commit()
        return game

    def create_player(self):
        player = Player(name="Alice")
        db.session.add(player)
        db.session.commit()
        return player