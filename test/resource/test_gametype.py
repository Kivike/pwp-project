import unittest
from sqlalchemy import exc
from sqlalchemy import orm

from src.app import create_app, db
from src.orm_models import GameType

import json
import random

ITEM_URL = "/api/gametypes/<gametype_name>/"
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
        """
        Test for retrieving nonexisting gametype
        Expecting 404 status code
        """
        url = ITEM_URL.replace("<gametype_name>", "Bridge")
        response = self.client.get(url)

        assert response.status_code == 404, response.status_code

    def testGetGametype(self):
        """
        Test for successful gametype retrieval
        """
        db.session.add(GameType(name="Chess"))
        db.session.commit

        url = ITEM_URL.replace("<gametype_name>", "Chess")
        response = self.client.get(url)

        assert response.status_code == 200, response.status_code

    def testGetGametypeCollection(self):
        response = self.client.get(COLLECTION_URL)

        assert response.status_code == 200, response.status_code
        assert response.data is not None
        json_object = json.loads(response.data)
        assert json_object is not None
        assert len(json_object['items']) == 0


        db.session.add(GameType(name="Chess"))
        db.session.add(GameType(name="Bridge"))
        db.session.commit()

        response = self.client.get(COLLECTION_URL)

        assert response.status_code == 200, response.status_code
        assert response.data is not None
        json_object = json.loads(response.data)
        assert json_object is not None
        assert len(json_object['items']) == 2, len(json_object['items'])

    def testPostGametype(self):
        """
        Test for successful gametype adding
        """
        test_cases = [
            {
                "name": "Bridge1",
                "min_players": 3,
                "max_players": 7
            },
            {
                "name": "Bridge2",
                "min_players": 2
            },
            {
                "name": "Bridge3",
                "max_players": 6
            }
        ]

        expected_count = 0

        for test_case in test_cases:
            response = self.client.post(COLLECTION_URL, data=json.dumps(test_case), content_type="application/json")
            expected_count += 1
            assert response.status_code == 201, response.status_code
            assert GameType.query.count() == expected_count, GameType.query.count()
    
    def testPostGametypeInvalidSchema(self):
        """
        Test for trying to add an invalid gametype
        400 error expected
        """
        response = self.client.post(
            COLLECTION_URL,
            data={"shoe_size": 10},
            content_type="application/json"
        )

        assert response.status_code == 400, response.status_code
        assert GameType.query.count() == 0, GameType.query.count()

    def testPostGametypeInvalidContent(self):
        """
        Test for trying to add invalid content as gametype
        415 error expected
        """
        response = self.client.post(COLLECTION_URL, data="asdasd")

        assert response.status_code == 415, response.status_code
        assert GameType.query.count() == 0, GameType.query.count()

    def testPostGametypeDuplicate(self):
        """
        Test adding a duplicate of an already existing gametype
        409 error expected
        """
        db.session.add(GameType(name="Chess"))
        db.session.commit()

        post_data = {
            "name": "Chess"
        }
        response = self.client.post(
            COLLECTION_URL,
            data=json.dumps(post_data),
            content_type="application/json"
        )

        assert response.status_code == 409, response.status_code
        assert GameType.query.count() == 1, GameType.query.count()

    def testPostGametypeMissingContenttype(self):
        """
        Test for trying to add without content-type
        415 error expected
        """
        response = self.client.post(
            COLLECTION_URL,
            data=json.dumps({"name": "Chess"})
        )
        assert response.status_code == 415, response.status_code
        assert GameType.query.count() == 0, GameType.query.count()


    def testPutGametype(self):
        """
        Test for successful PUT gametype
        """
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

    def testPutGametypeDuplicate(self):
        """
        Test for changing a gametype's name to a duplicate
        409 error expected
        """
        db.session.add(GameType(name="Chess"))
        db.session.add(GameType(name="3D Chess"))
        db.session.commit()

        put_data = {
            "name": "3D Chess"
        }
        response = self.client.put(
            ITEM_URL.replace("<gametype_name>", "Chess"),
            data=json.dumps(put_data),
            content_type="application/json"
        )

        assert response.status_code == 409, response.status_code
        assert GameType.query.count() == 2, GameType.query.count()

    def testDeleteGametype(self):
        """
        Test for successfully deleting a gametype
        """
        db.session.add(GameType(name="Chess"))
        db.session.commit()

        url = ITEM_URL.replace("<gametype_name>", "Chess")
        response = self.client.delete(url)

        assert response.status_code == 204, response.status_code
        assert GameType.query.count() == 0, GameType.query.count()

    def testDeleteNonExistingGametype(self):
        """
        Test for failing to delete a nonexisting gametype
        404 error expected
        """
        db.session.add(GameType(name="Chess"))
        db.session.commit()
        
        url = ITEM_URL.replace("<gametype_name>", "imaginary type")
        response = self.client.delete(url)

        assert response.status_code == 404, response.status_code
        assert GameType.query.count() == 1, GameType.query.count()