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

    def test_get_non_existing_gametype(self):
        url = ITEM_URL.replace("<gametype_name>", "Bridge")
        response = self.client.get(url)

        assert response.status_code == 404, response.status_code

    def test_get_gametype(self):
        db.session.add(GameType(name="Chess"))
        db.session.commit

        url = ITEM_URL.replace("<gametype_name>", "Chess")
        response = self.client.get(url)

        assert response.status_code == 200, response.status_code

    def test_post_valid_gametype(self):
        test_cases = [
            {
                'min_players': 3,
                'max_players': 7
            },
            {
                'min_players': 2
            },
            {
                'max_players': 6
            },
        ]

        for test_case in test_cases:
            test_case["name"]  = "Bridge"

        response = self.client.post(COLLECTION_URL, data=json.dumps(test_case))

        assert response.status_code == 201, response.status_code
    
    def test_post_invalid_schema_gametype(self):
        response = self.client.post(COLLECTION_URL, data=dict(
            shoe_size=10
        ))

        assert response.status_code == 400, response.status_code

    def test_post_invalid_mediatype_gametype(self):
        response = self.client.post(COLLECTION_URL, data="asdasd")

        assert response.status_code == 415, response.status_code

    def test_post_duplicate_gametype(self):
        db.session.add(GameType(name="Chess"))
        db.session.commit()

        response = self.client.post(COLLECTION_URL, data=json.dumps(dict(
            name="Chess"
        )))

        assert response.status_code == 409, response.status_code