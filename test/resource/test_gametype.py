import unittest
from sqlalchemy import exc
from sqlalchemy import orm

from src.app import create_app, db
from src.orm_models import GameType

import json

ITEM_URL = "/api/gametype/<gametype_name>/"
COLLECTION_URL = "/api/gametypes/"

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

    def testGetNonExistingGametype(self):
        url = ITEM_URL.replace("<gametype_name>", "Bridge")
        response = self.client.get(url)

        assert response.status_code == 404, response.status_code

    def testGetGametype(self):
        db.session.add(GameType(name="Chess"))
        db.session.commit

        url = ITEM_URL.replace("<gametype_name>", "Chess")
        response = self.client.get(url)

        assert response.status_code == 200, response.status_code

    def testPostGametype(self):
        test_cases = [
            {
                "min_players": 3,
                "max_players": 7
            },
            {
                "min_players": 2
            },
            {
                "max_players": 6
            },
        ]

        for test_case in test_cases:
            test_case["name"]  = "Bridge"

        response = self.client.post(COLLECTION_URL, data=json.dumps(test_case))

        assert response.status_code == 201, response.status_code
        assert GameType.query.count() == 1
    
    def testPostGametypeInvalidSchema(self):
        response = self.client.post(
            COLLECTION_URL,
            data={"shoe_size": 10},
            content_type="application/json"
        )

        assert response.status_code == 400, response.status_code
        assert GameType.query.count() == 0

    def testPostGametypeInvalidContent(self):
        response = self.client.post(COLLECTION_URL, data="asdasd")

        assert response.status_code == 415, response.status_code
        assert GameType.query.count() == 0

    def testPostGametypeMissingContenttype(self):
        response = self.client.post(
            COLLECTION_URL,
            data=json.dumps({"name": "Chess"})
        )
        assert response.status_code == 415, response.status_code
        assert GameType.query.count() == 0

    def testPostGametypeDuplicate(self):
        db.session.add(GameType(name="Chess"))
        db.session.commit()

        response = self.client.post(
            COLLECTION_URL,
            data=json.dumps({"name": "Chess"}),
            content_type="application/json"
        )

        assert response.status_code == 409, response.status_code
        assert GameType.query.count() == 1

    def testPutGametype(self):
        db.session.add(GameType(name="Chess", max_players=2))
        db.session.commit()

        response = self.client.put(
            ITEM_URL.replace("<gametype_name>", "Chess"),
            data=json.dumps({"name": "Chess", "max_players": 3}),
            content_type="application/json"
        )

        assert response.status_code == 201, response.status_code

        game_type = GameType.query.filter_by(name="Chess").first()
        assert game_type.max_players == 3

    def testDeleteGametype(self):
        db.session.add(GameType(name="Chess"))
        db.session.commit

        url = ITEM_URL.replace("<gametype_name>", "Chess")
        response = self.client.delete(url)

        assert response.status_code == 204, response.status_code
        assert GameType.query.count() == 1

    def testDeleteNonExistingGametype(self):
        url = ITEM_URL.replace("<gametype_name>", "imaginary type")
        response = self.client.delete(url)

        assert response.status_code == 404, response.status_code
        assert GameType.query.count() == 1