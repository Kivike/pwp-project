import unittest
from sqlalchemy import exc
from sqlalchemy import orm

from src.app import create_app, db
from src.orm_models import Player, PlayerScore, GameType, Game

class TestPlayerScore(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def testCreateAndDeleteValidPlayerScore(self):
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

    def testDuplicateIdThrowsError(self):
        game = self.create_basic_game()

        player_1 = self.create_player("Player 1")
        player_score_1 = PlayerScore(player=player_1, game=game)
        db.session.add(player_1)
        db.session.add(player_score_1)
        db.session.commit()

        player_2 = self.create_player("Player 2")
        player_score_2 = PlayerScore(id=player_score_1.id, player=player_2, game=game)
        db.session.add(player_2)
        db.session.add(player_score_2)

        with self.assertRaises(orm.exc.FlushError):
            db.session.commit()

    def testPlayerDeletionDeletesPlayerScore(self):
        game = self.create_basic_game()

        player_1 = self.create_player("Player 1")
        player_score_1 = PlayerScore(player=player_1, game=game)
        db.session.add(player_1)
        db.session.add(player_score_1)
        db.session.commit()

        assert PlayerScore.query.count() == 1
        assert Player.query.count() == 2

        db.session.delete(player_1)
        db.session.commit()

        assert Player.query.count() == 1
        assert PlayerScore.query.count() == 0
        
    def testGameDeletionDeletesPlayerScore(self):
        game = self.create_basic_game()

        player_1 = self.create_player("Player 1")
        player_score_1 = PlayerScore(player=player_1, game=game)
        db.session.add(player_1)
        db.session.add(player_score_1)
        db.session.commit()

        assert Game.query.count() == 1
        assert PlayerScore.query.count() == 1

        db.session.delete(game)
        db.session.commit()

        assert Game.query.count() == 0
        assert PlayerScore.query.count() == 0

    def create_basic_game(self):
        game_type = GameType(name="chess", max_players=3)
        host = Player(name="Test player")
        game = Game(game_type=game_type, host=host, game_token="test")

        db.session.add(game_type)
        db.session.add(host)
        db.session.add(game)
        db.session.commit()
        return game

    def create_player(self, name="Alice"):
        player = Player(name=name)
        db.session.add(player)
        db.session.commit()
        return player
