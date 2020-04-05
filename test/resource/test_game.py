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
        """
        Test for successfully retrieving a specific game
        """
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

    def testGetGameCollection(self):
        """
        Test for successfully retrieving a collection of games
        """
        response = self.client.get(COLLECTION_URL)

        assert response.status_code == 200, response.status_code
        assert response.data is not None
        json_object = json.loads(response.data)
        assert json_object is not None
        assert len(json_object['items']) == 0

        host = Player(name="Alice")
        db.session.add(host)
        game_type = GameType(name="Korona")
        db.session.add(game_type)

        db.session.add(Game(host=host, game_type=game_type, game_token="test123"))
        db.session.add(Game(host=host, game_type=game_type, game_token="test1234"))
        db.session.commit()

        response = self.client.get(COLLECTION_URL)

        assert response.status_code == 200, response.status_code
        assert response.data is not None
        json_object = json.loads(response.data)
        assert json_object is not None
        assert len(json_object['items']) == 2, len(json_object['items'])

    def testPostGame(self):
        """
        Test for successfull game add
        """
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
        assert GameType.query.count() == 1

    def testPostGameWithoutHost(self):
        """
        Test for adding a game with missing required data (host)
        Error 400 expected
        """
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
        assert Game.query.count() == 0

    def testPostGameWithoutType(self):
        """
        Test for adding a game with missing required data (gametype)
        Error 400 expected
        """
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
        assert Game.query.count() == 0

    def testPostGameInvalidContent(self):
        """
        Test for posting invalid data as json
        Error 400 expected
        """
        response = self.client.post(
            COLLECTION_URL,
            data="notavalidjson",
            content_type='application/json'
        )
        assert response.status_code == 400, response.status_code
        assert Game.query.count() == 0

    def testPostGameInvalidContentType(self):
        """
        Test for trying to add game with invalid content type
        415 error expected
        """
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
        assert Game.query.count() == 0

    def testPutGameValidRename(self):
        """
        Test for successfully renaming a game
        """
        host = Player(name="Alice")
        host_alter = Player(name="Bob")
        db.session.add(host)
        db.session.add(host_alter)

        game_type = GameType(name="Korona")
        game_type_alter = GameType(name="Blind Korona")
        db.session.add(game_type)
        db.session.add(game_type_alter)

        game = Game(host=host, game_type=game_type, game_token="test123")
        db.session.add(game)
        db.session.commit()

        url = ITEM_URL.replace("<game_token>", "test123")

        alter_data = {
            "host" : host_alter.name,
            "game_type": game_type_alter.name,
            "name": "test999"
        }

        response = self.client.put(
            url,
            data=json.dumps(alter_data),
            content_type="application/json"
        )

        assert response.status_code == 201, response.status_code
        game = Game.query.first()

        assert game.game_token == "test999", game.game_token
        assert game.host == host_alter, game.host
        assert game.game_type == game_type_alter, game.game_type
    
    def testPutNonExistingGame(self):
        host = Player(name="Alice")
        db.session.add(host)
        db.session.commit()

        put_data = {
            "host": "Alice",
            "game_type": "Korona"
        }
        url = ITEM_URL.replace("<game_token>", "doesnotexist")

        response = self.client.put(
            url,
            data=json.dumps(put_data),
            content_type="application/json"
        )

        assert response.status_code == 404, response.status_code

    def testPutGameNonExistingData(self):
        host = Player(name="Alice")
        db.session.add(host)

        game_type = GameType(name="Korona")
        db.session.add(game_type)

        game = Game(host=host, game_type=game_type, game_token="test123")
        db.session.add(game)
        db.session.commit()

        orig_data = {
            "host": "Alice",
            "game_type": "Korona",
            "name": "test123"
        }
        alter_data = {
            "host": "Bob",
            "game_type": "Uno"
        }
       
        for key in alter_data:
            put_data = orig_data.copy()
            put_data[key] = alter_data[key]

            url = ITEM_URL.replace("<game_token>", "test123")

            response = self.client.put(
                url,
                data=json.dumps(put_data),
                content_type="application/json"
            )
            assert response.status_code == 409, response.status_code

    def testDeleteGame(self):
        """
        Test for successful game deletion
        """
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
        assert Game.query.count() == 0

    def testDeleteNonExistingGame(self):
        """
        Test for error when deleting non existing game
        """
        url = ITEM_URL.replace("<game_token>", "doesnotexist")
        response = self.client.delete(url)

        assert response.status_code == 404, response.status_code