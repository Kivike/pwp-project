import unittest
import json

from sqlalchemy import exc
from sqlalchemy import orm

from src.app import create_app, db
from src.orm_models import Player

ITEM_URL = "/api/players/<player_name>/"
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

        assert response.status_code == 404, response.status_code

    def test_delete_non_existing_player(self):
        url = ITEM_URL.replace('<player_name>', 'idontexist')
        response = self.client.get(url)

        assert response.status_code == 404, response.status_code

    def test_post_valid_player(self):
        response = self.post_valid_player("Testaaja")

        assert response.status_code == 201, response.status_code

        player = Player.query.first()
        assert isinstance(player, Player)

    def test_delete_player(self):
        db.session.add(Player(name="Testaaja"))
        db.session.commit()

        delete_url = ITEM_URL.replace('<player_name>', 'Testaaja')
        response = self.client.delete(delete_url)

        assert response.status_code == 204, response.status_code

    def test_get_player_collection(self):
        response = self.client.get(COLLECTION_URL)

        assert response.status_code == 200, response.status_code
        assert response.data is not None
        json_object = json.loads(response.data)
        assert json_object is not None
        assert len(json_object['items']) == 0

        db.session.add(Player(name="Player A"))
        db.session.add(Player(name="Player B"))
        db.session.commit()

        response = self.client.get(COLLECTION_URL)

        assert response.status_code == 200, response.status_code
        assert response.data is not None
        json_object = json.loads(response.data)
        assert json_object is not None
        assert len(json_object['items']) == 2

    def test_get_player(self):
        player = Player(name="Testaaja")
        db.session.add(player)
        db.session.commit()

        get_url = ITEM_URL.replace("<player_name>", "Testaaja")
        response = self.client.get(get_url)

        assert response.data is not None
        json_object = json.loads(response.data)

        assert json_object is not None
        assert json_object["name"] == "Testaaja", json_object["name"]

    def test_put_player_valid_rename(self):
        player = Player(name="Testaaja")
        db.session.add(player)
        db.session.commit()

        edit_url = ITEM_URL.replace('<player_name>', 'Testaaja')
        response = self.client.put(
            edit_url,
            data=json.dumps({"name":"Newname"}),
            content_type='application/json'
        )

        assert response.status_code == 201, response.status_code

    def test_put_player_existing_name(self):
        self.post_valid_player("Player A")
        self.post_valid_player("Player B")

        edit_url = ITEM_URL.replace('<player_name>', 'Player A')
        response = self.client.put(
            edit_url,
            data=json.dumps({"name":"Player B"}),
            content_type=('application/json')
        )
        assert response.status_code == 409, response.status_code

    def test_put_player_invalid_schema(self):
        self.post_valid_player("Testaaja")

        edit_url = ITEM_URL.replace('<player_name>', 'Testaaja')
        response = self.client.put(
            edit_url,
            data=json.dumps({"color": "green"}),
            content_type='application/json'
        )
        assert response.status_code == 400, response.status_code

    def test_put_player_invalid_datatype(self):
        response = self.client.post(
            COLLECTION_URL,
            data='notavalidjson',
            content_type='application/json'
        )

        assert response.status_code == 415, response.status_code

    def post_valid_player(self, name):
        return self.client.post(
            COLLECTION_URL,
            data=json.dumps({"name": name}),
            content_type='application/json'
        )
        
