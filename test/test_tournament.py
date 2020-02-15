import unittest
from datetime import datetime
from sqlalchemy import exc

from src.app import create_app, db
from src.orm_models import Tournament, Game, GameType, Player

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

    def testCreateAndDeleteValidTournament(self):
        tournament = Tournament(name="Chess tournament")

        db.session.add(tournament)
        db.session.commit()

        assert Tournament.query.filter_by(name="Chess tournament").count() == 1
        tournament = Tournament.query.filter_by(name="Chess tournament").first()
        assert tournament.created_at is not None
        
        db.session.delete(tournament)
        db.session.commit()

        assert Tournament.query.count() == 0

    def testTournamentFinishedAt(self):
        tournament = Tournament(name="Test tournament", finished_at=datetime.fromisoformat('2020-02-15'))

        db.session.add(tournament)
        db.session.commit()

        assert Tournament.query.filter(Tournament.finished_at > '2020-02-01').count() == 1

    def testCreateTournamentWithoutName(self):
        tournament = Tournament()

        db.session.add(tournament)

        with self.assertRaises(exc.IntegrityError):
            db.session.commit()

    def testCreateTournamentWithSameName(self):
        tournament_1 = Tournament(name="Chess tournament")
        tournament_2 = Tournament(name="Chess tournament")

        db.session.add(tournament_1)
        db.session.add(tournament_2)

        with self.assertRaises(exc.IntegrityError):
            db.session.commit()

    def testTournamentStatus(self):
        tournament_1 = Tournament(name="Test tournament 1", status=0)
        tournament_2 = Tournament(name="Test tournament 2", status=0)
        tournament_3 = Tournament(name="Test tournament 3", status=1)

        db.session.add(tournament_1)
        db.session.add(tournament_2)
        db.session.add(tournament_3)
        db.session.commit()

        assert Tournament.query.filter_by(status=1).count() == 1

        tournament_2.status = 1
        db.session.add(tournament_2)
        db.session.commit()

        assert Tournament.query.filter_by(status=1).count() == 2