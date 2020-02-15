import unittest
from sqlalchemy import exc
from sqlalchemy import orm

from src.app import create_app, db
from src.orm_models import Player

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
        player = Player(name="Alice")

        db.session.add(player)
        db.session.commit()

        db_player = Player.query.first()
        assert db_player.name == "Alice"

        db.session.delete(db_player)
        db.session.commit()

        assert Player.query.first() == None

    def testCreatePlayerWithoutNameThrowsError(self):
        player = Player()

        db.session.add(player)

        with self.assertRaises(exc.IntegrityError):
            db.session.commit()

    def testCreatePlayerWithSameNameThrowsError(self):
        player_1 = Player(name="Alice")
        player_2 = Player(name="Alice")

        db.session.add(player_1)
        db.session.add(player_2)

        with self.assertRaises(exc.IntegrityError):
            db.session.commit()

    def testCreatePlayerWithSameIdThrowsError(self):
        player_1 = Player(name="Alice")

        db.session.add(player_1)
        db.session.commit()

        player_2 = Player(id=player_1.id, name="Bob")

        db.session.add(player_2)

        with self.assertRaises(orm.exc.FlushError):
            db.session.commit()

    def testDuplicatePlayerIdThrowsError(self):
        player_1 = Player()