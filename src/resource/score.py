from flask_restful import Resource, url_for
from flask import request, Response
from sqlalchemy.exc import IntegrityError
from src.utils import ScoreBuilder
from src.utils import create_error_response
from src.orm_models import PlayerScore, Game, Player
from src.extensions import db
import json
from jsonschema import validate, ValidationError

MASON = "application/vnd.mason+json"
NAMESPACE_URL = "/gamescore/link-relations#"
PROFILE_URL = "/profiles/score/"

class GameScoreboard(Resource):
    def get(self, game_name):
        items = []
        #Check whether game exists
        db_game = Game.query.filter_by(game_token=game_name).first()
        if db_game is None:
            return create_error_response(404, "Game not found")
        scores = PlayerScore.query.filter_by(game_id=db_game.id).all()
        if scores is None:
            return Response(status=204)
        for db_score in scores:
            player = db_score.player.name
            game = db_score.game.game_token
            body = ScoreBuilder(
                player = player,
                game = game
            )
            score = db_score.score
            if score is not None:
                body["score"] = score
            else:
                body["score"] = str(0.0)
            
            #Controls for an item
            body.add_control("self", url_for("playerscoreresource", game_name=game, player_name=player))
            body.add_control("profile", PROFILE_URL)
            items.append(body)

        body = ScoreBuilder()
        #Controls for collection
        body.add_namespace("gamescr", NAMESPACE_URL)
        body.add_control("self", url_for("gamescoreboard", game_name=game_name))
        body.add_control("up", url_for("gameresource", game_name=game_name))
        body.add_control_add_score(name=game_name)

        body["items"] = items

        return Response(json.dumps(body), 200, mimetype=MASON)

    def post(self, game_name):
        if not request.json:
            return create_error_response(415, "Unsupported Media Type", "use JSON")
        try: 
            validate(request.json, ScoreBuilder.scoreSchema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))
        score = PlayerScore(score = request.json["score"])
        db_game = Game.query.filter_by(game_token=game_name).first()
        if db_game is None:
            return create_error_response(409, "Game not found", 
                "Game with this name doesn't exist " + str(game_name))
        score.game_id = db_game.id
        db_player = Player.query.filter_by(name=request.json["player"]).first()
        if db_player is None:
            return create_error_response(409, "Player not found", 
                "Player with this name doesn't exist " + str(request.json["player"]))
        score.player_id = db_player.id

        #Check if player already has score in this game
        prevscores = PlayerScore.query.filter_by(game_id=db_game.id).filter_by(player_id=db_player.id).first()
        if prevscores is not None:
            return create_error_response(409, "Already exists", 
                    "Playerscore for this player already exists in game " + str(request.json["player"]))

        db.session.add(score)
        db.session.commit()

        return Response(status=201, headers={
            "Location": url_for("playerscoreresource", game_name=game_name, player_name=db_player.name)
            })
        

    
class PlayerScoreResource(Resource):
    def get(self, game_name, player_name):
        pass #TODO

    def put(self, game_name, player_name):
        pass #TODO

    def delete(self, game_name, player_name):
        pass #TODO