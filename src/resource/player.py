from flask_restful import Resource, url_for
from flask import request, Response
from sqlalchemy.exc import IntegrityError
from src.utils import PlayerBuilder
from src.utils import create_error_response
from src.orm_models import Player
from src.extensions import db
import json
from jsonschema import validate, ValidationError


MASON = "application/vnd.mason+json"
NAMESPACE_URL = "/gamescore/link-relations#"
PROFILE_URL = "/profiles/player/"

#Resource representing all the players
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

    #Add a new player 
    def post(self):
        if not request.json:
            return create_error_response(415, "Unsupported Media Type", "use JSON")
        try: 
            validate(request.json, PlayerBuilder.playerSchema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        player = Player(
            name = request.json["name"]
        )

        try: 
            db.session.add(player)
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists", "Player already exists with name " + str(request.json["name"]))

        return Response(status=201, headers={
            "Location": url_for("playerresource", player_name=request.json["name"])
        })
        

#Resource representing a single player
class PlayerResource(Resource):

    def get(self, player_name):
        db_player = Player.query.filter_by(name=player_name).first()
        if db_player is None:
            return create_error_response(404, "Player not found")
        body = PlayerBuilder(
                name = player_name
            )
        body.add_namespace("gamescr", NAMESPACE_URL)
        body.add_control("self", url_for("playerresource", player_name=player_name))
        body.add_control("profile", PROFILE_URL)
        body.add_control("collection", url_for("playercollection"))
        body.add_control_edit_player(name=player_name)
        body.add_control_leaderboard(name=player_name)
        body.add_control_delete_player(name=player_name)

        return Response(json.dumps(body), 200, mimetype=MASON)


        
    #Edit a player
    def put(self, player_name):
        if not request.json:
            return create_error_response(415, "Unsupported Media Type", "use JSON")
        db_player = Player.query.filter_by(name=player_name).first()
        if db_player is None:
            return create_error_response(404, "Player not found")
        try: 
            validate(request.json, PlayerBuilder.playerSchema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))
        
        new_name = request.json["name"]
        #If the new name already in use, return 409
        if new_name != player_name:
            db_player_new_name = Player.query.filter_by(name=new_name).first()
            if db_player_new_name is not None:
                return create_error_response(409, "Alredy exists", "Player already exists with name " + str(new_name))
        db_player.name = new_name
        db.session.add(db_player)
        db.session.commit()

        #Return the location in the header in case the name changes
        return Response(status=201, headers={
            "Location": url_for("playerresource", player_name=new_name)
        })


          
    #Delete a player
    def delete(self, player_name):
        db_player = Player.query.filter_by(name=player_name).first()
        if db_player is None:
            return create_error_response(404, "Player not found")
        db.session.delete(db_player)
        db.session.commit()

        return Response(status=204)
