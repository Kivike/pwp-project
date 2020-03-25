from flask_restful import Resource, url_for
from flask import request, Response
from sqlalchemy.exc import IntegrityError
from src.utils import GametypeBuilder
from src.utils import create_error_response
from src.orm_models import GameType
from src.extensions import db
import json
from jsonschema import validate, ValidationError

MASON = "application/vnd.mason+json"
NAMESPACE_URL = "/gamescore/link-relations#"
PROFILE_URL = "/profiles/gametype/"

class GametypeCollection(Resource):
    def get(self):
        items = []
        gametypes = GameType.query.all()
        if gametypes is None:
            return Response(status=204)
        for db_gametype in gametypes:
            name = db_gametype.name
            body = GametypeBuilder(
                name = name
            )
            max_players = db_gametype.max_players
            if max_players is not None:
                body["max_players"] = max_players
            min_players = db_gametype.min_players
            if min_players is not None:
                body["min_players"] = min_players

            #Controls for an item
            body.add_control("self", url_for("gametyperesource", gametype_name=name))
            body.add_control("profile", PROFILE_URL)
            items.append(body)

        body = GametypeBuilder()
        #Controls for collection
        body.add_namespace("gamescr", NAMESPACE_URL)
        body.add_control("self", url_for("gametypecollection"))
        body.add_control_add_gametype()
        body.add_control_all_games()
        body["items"] = items

        return Response(json.dumps(body), 200, mimetype=MASON)
            

    def post(self):
        if not request.json:
            return create_error_response(415, "Unsupported Media Type", "use JSON")
        try: 
            validate(request.json, GametypeBuilder.gametypeSchema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        gametype = GameType(
            name = request.json["name"]
        )
        if "min_players" in request.json:
            gametype.min_players = request.json["min_players"]
        if "max_players" in request.json:
            gametype.max_players = request.json["max_players"]

        try: 
            db.session.add(gametype)
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists", 
                "Gametype with this name already exists " + str(request.json["name"]))

        return Response(status=201, headers={
            "Location": url_for("gametyperesource", gametype_name=request.json["name"])
            })

class GametypeResource(Resource):
    def get(self, gametype_name):
        pass #TODO

    def put(self, gametype_name):
        pass #TODO

    def delete(self, gametype_name):
        pass #TODO