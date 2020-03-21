from flask_restful import Resource, url_for
from src.utils import *
from src.orm_models import Player

NAMESPACE_URL = "/gamescore/link-relations#"
PROFILE_URL = "/profiles/player/"

class PlayerCollection(Resource):
    def get(self):
        items = []
        players = Player.query.all()
        for player in players:
            name = player.name
            body = PlayerBuilder(
                name = name
            )
            body.add_control("self", url_for("playerresource", player_name=name))
            body.add_control("profile", PROFILE_URL)
            items.append(body)
        body = PlayerBuilder()
        body.add_namespace("gamescr", NAMESPACE_URL)
        body.add_control("self", url_for("playercollection"))
        body.add_control_all_games()
        body.add_control_all_tournaments()
        body.add_control_add_player()
        body["items"] = items

        return Response(json.dumps(body), 200, mimetype=MASON)


    def post(self):
        pass #TODO

class PlayerResource(Resource):
    def get(self, player_name):
        pass #TODO

    def put(self, player_name):
        pass #TODO

    def delete(self, player_name):
        pass #TODO