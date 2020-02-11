import unittest
import numbers
from app import create_app, db
from orm_models import GameType, Player, Game, PlayerScore

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

    def testCreateBasicGame(self):
        self.create_basic_game()

        assert Game.query.count() == 1
        
        db_game = Game.query.first()
        db_player = Player.query.first()
        db_game_type = GameType.query.first()

        assert db_game.host_id == db_player.id
        assert db_game.game_type_id == db_game_type.id

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

    def create_basic_game(self):
        game_type = GameType(name="chess", max_players=3)
        host = Player(name="Test player")
        game = Game(status=1, game_type=game_type, host=host)

        db.session.add(game_type)
        db.session.add(host)
        db.session.add(game)
        db.session.commit()

if __name__ == '__main__':
    unittest.main()
    