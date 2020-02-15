import unittest
from unittest_data_provider import data_provider
from sqlalchemy import exc

from src.app import create_app, db
from src.orm_models import GameType

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

    # min_players, max_players
    player_count_cases = [
        (None, None), (None, 2), (10, None)
    ]

    def testCreateAndDeleteValidGameType(self):
        game_type = GameType(name="Hearts")

        for min_players, max_players in self.player_count_cases:
            with self.subTest():
                if (max_players is not None):
                    game_type.max_players = max_players

                if (min_players is not None):
                    game_type.min_players = min_players

                db.session.add(game_type)
                db.session.commit()

                assert GameType.query.filter_by(name="Hearts").count() == 1
                
    def testCreateGameTypeWithoutName(self):
        game_type = GameType()

        db.session.add(game_type)

        with self.assertRaises(exc.IntegrityError):
            db.session.commit()

    def testCreateGameWithSameName(self):
        game_type_1 = GameType(name="Hearts")
        game_type_2 = GameType(name="Hearts")

        db.session.add(game_type_1)
        db.session.add(game_type_2)

        with self.assertRaises(exc.IntegrityError):
            db.session.commit()

    def testUpdateMaxPlayers(self):
        game_type = GameType(name="Hearts")

        db.session.add(game_type)
        db.session.commit()

        db_game_type = GameType.query.filter_by(name="Hearts").first()

        assert db_game_type.min_players == None
        assert db_game_type.max_players == None

        game_type.min_players = 3
        game_type.max_players = 4

        db.session.add(game_type)
        db.session.commit()

        db_game_type = GameType.query.filter_by(name="Hearts").first()

        assert db_game_type.min_players == 3
        assert db_game_type.max_players == 4