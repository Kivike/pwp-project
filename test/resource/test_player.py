import unittest
from sqlalchemy import exc
from sqlalchemy import orm

from src.app import create_app, db
from src.orm_models import GameType

import json

ITEM_URL = "/api/player/<player_name>/"
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

    def test_get_non_existing_player(self):
        url = ITEM_URL.replace('<player_name>', 'idontexist')
        response = self.client.get(url)

        assert response.status_code == 404

    def test_delete_non_existing_player(self):
        url = ITEM_URL.replace('<player_name>', 'idontexist')
        response = self.client.get(url)

        assert response.status_code == 404

    def test_create_and_delete_player(self):
        create_response = self.client.post(COLLECTION_URL, data=dict(
            name="Testaaja"
        ))

        assert create_response.status_code == 201

        delete_url = ITEM_URL.replace('<player_name>', 'Testaaja')
        delete_response = self.client.delete(delete_url)

        assert delete_response.status_code == 204

    def test_get_player_collection(self):
        response = self.client.get(COLLECTION_URL)

        assert response.status_code == 200
        assert response.data is not None
        json_object = json.loads(response.data)
        assert json_object is not None
        assert len(json_object['items']) == 0

        self.client.post(COLLECTION_URL, data=dict(
            name="Player A"
        ))
        self.client.post(COLLECTION_URL, data=dict(
            name="Player B"
        ))

        response = self.client.get(COLLECTION_URL)

        assert response.status_code == 200
        assert response.data is not None
        json_object = json.loads(response.data)
        assert json_object is not None
        assert len(json_object['items']) == 2

    def test_get_player(self):
        self.client.post(COLLECTION_URL, data=dict(
            name="Testaaja"
        ))

        get_url = ITEM_URL.replace("<player_name>", "Testaaja")
        response = self.client.get(get_url)

        assert response.data is not None
        json_object = json.loads(response.data)

        assert json_object is not None
        assert len(json_object["name"]) == "Testaaja"

    def test_valid_rename_player(self):
        self.client.post(COLLECTION_URL, data=dict(
            name="Testaaja"
        ))

        edit_url = ITEM_URL.replace('<player_name>', 'Testaaja')
        response = self.client.put(edit_url, data=dict(
            name="Newname"
        ))

        assert response.status_code == 204

    def test_rename_player_existing_name(self):
        self.client.post(COLLECTION_URL, data=dict(
            name="Player A"
        ))
        self.client.post(COLLECTION_URL, data=dict(
            name="Player B"
        ))

        edit_url = ITEM_URL.replace('<player_name>', 'Player A')
        response = self.client.put(edit_url, data=dict(
            name="Player B"
        ))
        assert response.status_code == 409

    def test_edit_player_invalid_schema(self):
        self.client.post(COLLECTION_URL, data=dict(
            name="Testaaja"
        ))
        edit_url = ITEM_URL.replace('<player_name>', 'Testaaja')
        response = self.client.put(edit_url, data=dict(
            color="green"
        ))
        assert response.status_code == 400