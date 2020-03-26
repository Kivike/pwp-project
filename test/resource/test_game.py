import unittest
from sqlalchemy import exc
from sqlalchemy import orm

from src.app import create_app, db
from src.orm_models import Game, Player, GameType

import json

ITEM_URL = "/api/games/<game_token>/"
COLLECTION_URL = "/api/games/"

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

    def testGetNonExistingGame(self):
        url = ITEM_URL.replace("<game_token>", "doesnotexist123")
        response = self.client.get(url)

        assert response.status_code == 404, response.status_code

    def testGetGame(self):
        host = Player(name="Alice")
        db.session.add(host)

        game_type = GameType(name="Korona")
        db.session.add(game_type)

        game = Game(host=host, game_type=game_type, game_token="test123")
        db.session.add(game)
        db.session.commit()

        url = ITEM_URL.replace('<game_token>', "test123")
        response = self.client.get(url)

        assert response.status_code == 200, response.status_code

    def testPostGame(self):
        host = Player(name="Alice")
        db.session.add(host)

        game_type = GameType(name="Korona")
        db.session.add(game_type)
        db.session.commit()

        game_data = {
            "host": "Alice",
            "game_type": "Korona",
        }

        response = self.client.post(
            COLLECTION_URL,
            data=json.dumps(game_data),
            content_type='application/json'
        )
        assert response.status_code == 201, response.status_code

    def testPostGameWithoutHost(self):
            game_type = GameType(name="Korona")
            db.session.add(game_type)
            db.session.commit()

            game_data = {
                "game_type": "Korona"
            }
            response = self.client.post(
                COLLECTION_URL,
                data=json.dumps(game_data),
                content_type='application/json'
            )
            assert response.status_code == 400, response.status_code

    def testPostGameWithoutType(self):
        host = Player(name="Alice")
        db.session.add(host)
        db.session.commit()

        game_data = {
            "host": "Alice"
        }
        response = self.client.post(
            COLLECTION_URL,
            data=json.dumps(game_data),
            content_type='application/json'
        )
        assert response.status_code == 400, response.status_code

    def testPostGameInvalidContent(self):
        response = self.client.post(
            COLLECTION_URL,
            data="notavalidjson",
            content_type='application/json'
        )
        assert response.status_code == 415, response.status_code

    def testPostGameInvalidContentType(self):
        host = Player(name="Alice")
        db.session.add(host)

        game_type = GameType(name="Korona")
        db.session.add(game_type)
        db.session.commit()

        game_data = {
            "host": "Alice",
            "game_type": "Korona",
        }
        response = self.client.post(
            COLLECTION_URL,
            data=json.dumps(game_data)
        )
        assert response.status_code == 415, response.status_code
    
    def testDeleteGame(self):
        host = Player(name="Alice")
        db.session.add(host)

        game_type = GameType(name="Korona")
        db.session.add(game_type)

        game = Game(host=host, game_type=game_type, game_token="test123")
        db.session.add(game)
        db.session.commit()

        url = ITEM_URL.replace("<game_token>", "test123")
        response = self.client.delete(url)

        assert response.status_code == 204, response.status_code

    def testDeleteNonExistingGame(self):
        url = ITEM_URL.replace("<game_token>", "doesnotexist")
        response = self.client.delete(url)

        assert response.status == 404, response.status_code