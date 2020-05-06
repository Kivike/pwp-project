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
            db.session.rollback()
            return create_error_response(409, "Already exists", 
                "Gametype with this name already exists " + str(request.json["name"]))

        return Response(status=201, headers={
            "Location": url_for("gametyperesource", gametype_name=request.json["name"])
            })

class GametypeResource(Resource):
    def get(self, gametype_name):
        #Check whether gametype exists
        db_gametype = GameType.query.filter_by(name=gametype_name).first()
        if db_gametype is None:
            return create_error_response(404, "Gametype not found")
        
        body = GametypeBuilder(
            name = gametype_name
        )
        min_players = db_gametype.min_players

        #Check whether game type has min_players or max_players set
        if min_players is not None:
            body["min_players"] = min_players
        max_players = db_gametype.max_players
        if max_players is not None:
            body["max_players"] = max_players
        body.add_namespace("gamescr", NAMESPACE_URL)
        body.add_control("self", url_for("gametyperesource", gametype_name=gametype_name))
        body.add_control("profile", PROFILE_URL)
        body.add_control("collection", url_for("gametypecollection"))
        body.add_control_edit_gametype(name=gametype_name)
        body.add_control_leaderboard(name=gametype_name)
        body.add_control_delete_gametype(name=gametype_name)

        return Response(json.dumps(body), 200, mimetype=MASON)

    #Edit a gametype
    def put(self, gametype_name):
        if not request.json:
            return create_error_response(415, "Unsupported Media Type", "use JSON")
        nameChange = False
        db_gametype = GameType.query.filter_by(name=gametype_name).first()
        if db_gametype is None:
            return create_error_response(404, "Gametype not found")
        try: 
            validate(request.json, GametypeBuilder.gametypeSchema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))
        
        new_name = request.json["name"]
        #If the new name already in use, return 409
        if new_name != gametype_name:
            nameChange = True
            db_gametype_new_name = GameType.query.filter_by(name=new_name).first()
            if db_gametype_new_name is not None:
                return create_error_response(409, "Already exists", "Gametype already exists with name "
                    + str(new_name))
        db_gametype.name = new_name
        #if min_players specified in the request
        try:
            new_min_players = request.json["min_players"]
            db_gametype.min_players = new_min_players
        except KeyError:
            #min_players not specified, set to null
            db_gametype.min_players = None
        #if max_players specificed in the request
        try:
            new_max_players = request.json["max_players"]
            db_gametype.max_players = new_max_players
        except KeyError:
            #max_players not specified, set to null
            db_gametype.max_players = None
        db.session.add(db_gametype)
        db.session.commit()

        #Return the location in the header in case the name changes
        if nameChange:
            return Response(status=201, headers={
                "Location": url_for("gametyperesource", gametype_name=new_name)
            })
        else:
            return Response(status=204)

    #Delete a gametype
    def delete(self, gametype_name):
        db_gametype = GameType.query.filter_by(name=gametype_name).first()
        if db_gametype is None:
            return create_error_response(404, "Gametype not found")
        db.session.delete(db_gametype)
        db.session.commit()

        return Response(status=204)