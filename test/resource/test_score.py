import unittest
from sqlalchemy import exc
from sqlalchemy import orm

from src.app import create_app, db
from src.orm_models import Player

import json

SCOREBOARD_URL = "/api/games/<game_token>/scoreboard"
COLLECTION_URL = "/api/players/"

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def testGetNonExistingGameScoreboard(self):
        url = SCOREBOARD_URL.replace('<game_token>', 'doesnotexist123')
        response = self.client.get(url)
        
        assert response.status_code == 404, response.status_code
