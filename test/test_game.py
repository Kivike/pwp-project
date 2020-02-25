import unittest
import numbers

from sqlalchemy import exc
from sqlalchemy import orm

from src.app import create_app, db
from src.orm_models import GameType, Player, Game, PlayerScore

class TestGame(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def testCreateAndDeleteValidGame(self):
        self.create_basic_game()

        assert Game.query.count() == 1
        
        db_game = Game.query.first()
        db_player = Player.query.first()
        db_game_type = GameType.query.first()

        assert db_game.host_id == db_player.id
        assert db_game.game_type_id == db_game_type.id
        assert db_game.created_at is not None

        db.session.delete(db_game)
        db.session.commit()

        assert Game.query.count() == 0

    def testCreateGameWithoutGameTypeThrowsError(self):
        host = Player(name="Test player")
        game = Game(host=host, game_token="12345")

        db.session.add(host)
        db.session.add(game)
        db.session.commit()

        assert Game.query.count() == 1

    def testFinishGame(self):
        game = self.create_basic_game()

    def testCreateGameWithoutHostThrowsError(self):
        game_type = GameType(name="chess")
        game = Game(game_type = game_type, game_token="12345")

        db.session.add(game_type)
        db.session.add(game)
        db.session.commit()

        assert Game.query.count() == 1

    def testAssignPlayerScoresToGame(self):
        self.create_basic_game()
        db_game = Game.query.first()

        host = db_game.host

        player_a = Player(name="Test player A")
        player_b = Player(name="Test player B")

        host_score = PlayerScore(player=host, game=db_game)
        player_score_a = PlayerScore(player=player_a, game=db_game)
        player_score_b = PlayerScore(player=player_b, game=db_game)

        db_game.scores.append(host_score)
        db_game.scores.append(player_score_a)
        db_game.scores.append(player_score_b)

        db.session.add(db_game)
        db.session.commit()

        db_game = Game.query.first()
        assert len(db_game.scores) == 3

        db_game.scores.remove(player_score_a)

        db.session.delete(player_score_a)
        db.session.add(db_game)
        db.session.commit()
        assert len(Game.query.first().scores) == 2

    def testDuplicateIdThrowsError(self):
        game = self.create_basic_game()

        game_duplicate = Game(id=game.id, game_type=game.game_type, host=game.host)

        db.session.add(game_duplicate)
        
        with self.assertRaises(orm.exc.FlushError):
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

if __name__ == '__main__':
    unittest.main()
    