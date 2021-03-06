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

    def testGetNonExistingPlayer(self):
        '''
        Test for getting player that does not exist in database
        Expects HTTP code 404 as response
        '''
        url = ITEM_URL.replace('<player_name>', 'idontexist')
        response = self.client.get(url)

        assert response.status_code == 404, response.status_code

    def testPostValidPlayer(self):
        '''
        Test creating a player with valid data
        Expects HTTP code 201 (Created) and that a player will be created to database
        '''
        response = self.client.post(
            COLLECTION_URL,
            data=json.dumps({"name": "Testaaja"}),
            content_type='application/json'
        )
        assert response.status_code == 201, response.status_code

        player = Player.query.first()
        assert isinstance(player, Player)

    def testPostPlayerDuplicateName(self):
        '''
        Test creating player with name that is already in use by another player
        Expects HTTP code 409 (Conflict) as response
        '''
        db.session.add(Player(name="Testaaja"))
        db.session.commit()

        response = self.client.post(
            COLLECTION_URL,
            data=json.dumps({"name": "Testaaja"}),
            content_type='application/json'
        )

        assert response.status_code == 409, response.status_code

    def testPostPlayerInvalidSchema(self):
        '''
        Test creating player with invalid fields in body
        Expects HTTP code 400 (Bad Request) as reponse
        '''
        response = self.client.post(
            COLLECTION_URL,
            data=json.dumps({"foot_size": 123}),
            content_type="application/json"
        )
        assert response.status_code == 400, response.status_code
        assert Player.query.count() == 0

    def testDeleteExistingPlayer(self):
        '''
        Test deleting a player that exists in database
        Expects HTTP code 204 (No Content) as response
        '''
        db.session.add(Player(name="Testaaja"))
        db.session.commit()

        delete_url = ITEM_URL.replace('<player_name>', 'Testaaja')
        response = self.client.delete(delete_url)

        assert response.status_code == 204, response.status_code
        assert Player.query.count() == 0, Player.query.count()

    def testDeleteNonExistingPlayer(self):
        '''
        Test deleting a player that does not exist in database
        Expects HTTP code 404 (Not Found) as response
        '''
        delete_url = ITEM_URL.replace('<player_name>', 'Santa Claus')
        response = self.client.delete(delete_url)

        assert response.status_code == 404, response.status_code

    def testGetEmptyPlayerCollection(self):
        '''
        Test getting player collection when there are no players in database
        Expects HTTP code 200 (OK) as response and response contains empty item list
        '''
        response = self.client.get(COLLECTION_URL)

        assert response.status_code == 200, response.status_code
        assert response.data is not None
        json_object = json.loads(response.data)
        assert json_object is not None
        assert len(json_object['items']) == 0

    def testGetPlayerCollectionWithItems(self):
        '''
        Test getting player collection when there are players in database
        Expects HTTP code 200 (OK) as and body with list of players in database as response
        '''
        db.session.add(Player(name="Player A"))
        db.session.add(Player(name="Player B"))
        db.session.commit()

        response = self.client.get(COLLECTION_URL)

        assert response.status_code == 200, response.status_code
        assert response.data is not None
        json_object = json.loads(response.data)
        assert json_object is not None
        assert len(json_object['items']) == 2, len(json_object['items'])

    def testGetExistingPlayer(self):
        '''
        Test getting player that exists in database
        Expects HTTP code 200 (OK) and body with player as response
        '''
        player = Player(name="Testaaja")
        db.session.add(player)
        db.session.commit()

        get_url = ITEM_URL.replace("<player_name>", "Testaaja")
        response = self.client.get(get_url)

        assert response.status_code == 200, response.status_code
        assert response.data is not None
        json_object = json.loads(response.data)

        assert json_object is not None
        assert json_object["name"] == "Testaaja", json_object["name"]

    def testPutPlayerValidRename(self):
        '''
        Test renaming player to a name that is not taken by another player
        Expects HTTP code 201 (Created) and that player is renamed in database
        '''
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
        assert Player.query.filter_by(name="Newname").count() == 1, Player.query.filter_by(name="Newname").count()

    def testPutPlayerExistingName(self):
        '''
        Test renaming player to a name that is taken by another player
        Expects HTTP code 409 (Conflict) as reponse, and that player name is not changed
        '''
        db.session.add(Player(name="Player A"))
        db.session.add(Player(name="Player B"))
        db.session.commit()

        edit_url = ITEM_URL.replace('<player_name>', 'Player A')
        response = self.client.put(
            edit_url,
            data=json.dumps({"name":"Player B"}),
            content_type=('application/json')
        )
        assert response.status_code == 409, response.status_code
        assert Player.query.filter_by(name="Player A").count() == 1, Player.query.filter_by(name="Player A").count()
        assert Player.query.filter_by(name="Player B").count() == 1, Player.query.filter_by(name="Player B").count()

    def testPutPlayerInvalidSchema(self):
        '''
        Test updating player with invalid fields
        Expects HTTP code 400 (Bad Request) as response
        '''
        player = Player(name="Testaaja")
        db.session.add(player)
        db.session.commit()

        edit_url = ITEM_URL.replace('<player_name>', 'Testaaja')
        response = self.client.put(
            edit_url,
            data=json.dumps({"color": "green"}),
            content_type="application/json"
        )
        assert response.status_code == 400, response.status_code
        assert Player.query.count() == 1, Player.query.count()

    def testPutPlayerInvalidDatatype(self):
        '''
        Test updating player with invalid JSON as body
        Expects HTTP code 400 (Bad Request) as response
        '''
        player = Player(name="Testaaja")
        db.session.add(player)
        db.session.commit()

        edit_url = ITEM_URL.replace('<player_name>', 'Testaaja')
        response = self.client.put(
            edit_url,
            data="{////SDGF}",
            content_type='application/json'
        )

        assert response.status_code == 400, response.status_code

    def testPutPlayerMissingContenttype(self):
        '''
        Test updating player with no content type header not set
        Expects HTTP code 415 (Unsupported Media Type) as response
        '''
        player = Player(name="Testaaja")
        db.session.add(player)
        db.session.commit()

        edit_url = ITEM_URL.replace('<player_name>', 'Testaaja')
        response = self.client.put(
            edit_url,
            data=json.dumps({"name": "Testaaja ABC"})
        )
        assert response.status_code == 415, response.status_code
