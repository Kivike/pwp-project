from flask_restful import Resource, url_for
from flask import request, Response
from sqlalchemy.exc import IntegrityError
from src.utils import GameBuilder
from src.utils import create_error_response
from src.orm_models import Game, GameType, Player, Tournament
from src.extensions import db
import json
import random
import string
from jsonschema import validate, ValidationError
import datetime

MASON = "application/vnd.mason+json"
NAMESPACE_URL = "/gamescore/link-relations#"
PROFILE_URL = "/profiles/game/"

class GameCollection(Resource):
    def get(self):
        items = []
        games = Game.query.all()
        
        for db_game in games:
            name = db_game.game_token
            status = db_game.status
            body = GameBuilder(
                name = name,
                status = status
            )
            gametype = db_game.game_type
            if gametype is not None:
                body["game_type"] = gametype.name
            host = db_game.host
            if host is not None:
                body["host"] = host.name
            tournament = db_game.tournament
            if tournament is not None:
                body["tournament"] = tournament.name
            body["created"] = str(db_game.created_at)
            finished = db_game.finished_at
            if finished is not None:
                body["finished"] = str(finished)

            #Controls for an item
            body.add_control("self", url_for("gameresource", game_name=name))
            body.add_control("profile", PROFILE_URL)
            items.append(body)

        body = GameBuilder()
        #Controls for collection
        body.add_namespace("gamescr", NAMESPACE_URL)
        body.add_control("self", url_for("gamecollection"))
        body.add_control_all_gametypes()
        body.add_control_all_tournaments()
        body.add_control_all_players()
        body.add_control_add_game()
        body["items"] = items

        return Response(json.dumps(body), 200, mimetype=MASON)

    def post(self):
        if not request.json:
            return create_error_response(415, "Unsupported Media Type", "use JSON")
        try: 
            validate(request.json, GameBuilder.gameSchema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        db_gametype = GameType.query.filter_by(name=request.json["game_type"]).first()
        if db_gametype is None:
            return create_error_response(409, "Gametype not found", 
                "Gametype with this name doesn't exist " + str(request.json["game_type"]))
        game = Game(game_type_id = db_gametype.id)
        db_host = Player.query.filter_by(name=request.json["host"]).first()
        if db_host is None:
            return create_error_response(409, "Host not found", 
                "Player with this name doesn't exist " + str(request.json["host"]))
        game.host_id = db_host.id
        if "status" in request.json:
            game.status = request.json["status"]
        if "tournament" in request.json:
            db_tournament = Tournament.query.filter_by(name=request.json["tournament"]).first()
            if db_tournament is None:
                return create_error_response(409, "Tournament not found", 
                "Tournament with this name doesn't exist " + str(request.json["tournament"]))
            game.tournament_id = db_tournament.id
        
        #Name is either decided by the user or generated from gametype
        if "name" in request.json:
            game.game_token = request.json["name"]
            try: 
                db.session.add(game)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return create_error_response(409, "Already exists", 
                    "Game with this name already exists " + str(request.json["name"]))
        else:
            limiter = 0
            while True:
                if limiter > 10:
                    return Response(status=507, response="Unexpected error, please name game manually")
                game.game_token = request.json["game_type"] + ''.join(random.choices(string.ascii_lowercase+string.digits, k = 6))
                try: 
                    limiter += 1
                    db.session.add(game)
                    db.session.commit()
                    break
                except IntegrityError:
                    continue


        return Response(status=201, headers={
            "Location": url_for("gameresource", game_name=game.game_token)
            })

        

class GameResource(Resource):

    #Get a game 
    def get(self, game_name):
        #Check whether game exists
        db_game = Game.query.filter_by(game_token=game_name).first()
        if db_game is None:
            return create_error_response(404, "Game not found")
        
        body = GameBuilder(
            name = db_game.game_token,
            status = db_game.status,
            created = str(db_game.created_at)
        )
        #Get game_type if exists
        if db_game.game_type is not None:
            body["game_type"] = db_game.game_type.name
        
        #Get host if exists
        if db_game.host is not None:
            body["host"] = db_game.host.name
        
        #Get tournament if exists
        if db_game.tournament is not None:
            body["tournament"] = db_game.tournament.name
        if db_game.finished_at is not None:
            body["finished"] = str(db_game.finished_at)
        body.add_namespace("gamescr", NAMESPACE_URL)
        body.add_control("self", url_for("gameresource", game_name=game_name))
        body.add_control("profile", PROFILE_URL)
        body.add_control("collection", url_for("gamecollection"))
        if db_game.game_type is not None:
            body.add_control_gametype(name=db_game.game_type.name)
        body.add_control_all_players()
        body.add_control_scores(name=game_name)
        if db_game.tournament is not None:
            body.add_control_tournament(name=db_game.tournament.name)
        body.add_control_add_score(name=game_name)
        body.add_control_edit_game(name=game_name)
        body.add_control_delete_game(name=game_name)
        
        return Response(json.dumps(body), 200, mimetype=MASON)


    #Edit a game
    def put(self, game_name):
        if not request.json:
            return create_error_response(415, "Unsupported Media Type", "use JSON")
        db_game = Game.query.filter_by(game_token=game_name).first()
        if db_game is None:
            return create_error_response(404, "Game not found")
        try: 
            validate(request.json, GameBuilder.gameSchema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))
        if "name" in request.json:
            new_name = request.json["name"]
            #If the new name already in use, return 409
            if new_name != game_name:
                db_game_new_name = Game.query.filter_by(game_token=new_name).first()
                if db_game_new_name is not None:
                    return create_error_response(409, "Alredy exists", "Game already exists with name "
                        + str(new_name))
            db_game.game_token = new_name

        #if status changes from 1 to 0 (game ends) or 0 to 1 (game is active again), log the time the game ends/
        #remove it
        if "status" in request.json:
            new_status = request.json["status"]
            if db_game.finished_at is None:
                if new_status == 0:
                    db_game.finished_at = datetime.datetime.now()
            else:
                if new_status == 1:
                    db_game.finished_at = None
            db_game.status = new_status
        else:
            if db_game.finished_at is not None:
                db_game.finished_at = None

        #If gametype updated, check that it is valid
        new_gametype = request.json["game_type"]
        
        db_new_gametype = GameType.query.filter_by(name=new_gametype).first()
        if db_new_gametype is None:
            return create_error_response(409, "Gametype not valid", "No gametype exists with name "
                + str(new_gametype))
        else:
            db_game.game_type = db_new_gametype
        
        #If host name updated, check that it is valid
        new_host_name = request.json["host"]

        db_new_host = Player.query.filter_by(name=new_host_name).first()
        if db_new_host is None:
            return create_error_response(409, "Host name not valid", "No player exists with name "
                + str(new_host_name))
        else:
            db_game.host = db_new_host

        #If tournament updated, check that is valid
        if "tournament" in request.json:
            new_tournament_name = request.json["tournament"]
            db_new_tournament = Tournament.query.filter_by(name=new_tournament_name).first()
            if db_new_tournament is None:
                return create_error_response(409, "Tournament name not valid", "No tournament exists with name "
                    + str(new_tournament_name))
            else:
                db_game.tournament = db_new_tournament
        else:
             db_game.tournament = None
               
        db.session.add(db_game)
        db.session.commit()

        #Return the location in the header in case the name changes
        return Response(status=201, headers={
            "Location": url_for("gameresource", game_name=db_game.game_token)
        })



        
    #Delete a game
    def delete(self, game_name):
        db_game = Game.query.filter_by(game_token=game_name).first()
        if db_game is None:
            return create_error_response(404, "Game not found")
        db.session.delete(db_game)
        db.session.commit()

        return Response(status=204)
