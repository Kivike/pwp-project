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
        pass #TODO

    def post(self, game_name):
        pass #TODO
    
class PlayerScoreResource(Resource):
    
    def get(self, game_name, player_name):
        db_game = Game.query.filter_by(game_token=game_name).first()
        if db_game is None:
            return create_error_response(404, "No game found with name " + str(game_name))
        db_player = Player.query.filter_by(name=player_name).first()
        if db_player is None:
            return create_error_response(404, "No player found with name " + str(player_name))
        db_player_score = PlayerScore.query.filter_by(player=db_player, game=db_game).first()
        if db_player_score is None:
            return create_error_response(404, "No score found with player name " + str(player_name)
                + " and game name " + str(game_name))
        
        body = ScoreBuilder(
            name = db_player.name,
            game = db_game.game_token
        )
        if db_player_score.score is not None:
            body["score"] = db_player_score.score
        body.add_namespace("gamescr", NAMESPACE_URL)
        body.add_control("self", url_for("playerscoreresource", game_name=game_name, player_name=player_name))
        body.add_control("profile", PROFILE_URL)
        body.add_control("collection", url_for("gamescoreboard", game_name=game_name))
        body.add_control_edit_playerscore(game_name=game_name, player_name=player_name)
        body.add_control_delete_playerscore(game_name=game_name, player_name=player_name)
        body.add_control_player(player_name=player_name)

        return Response(json.dumps(body), 200, mimetype=MASON)

    #Edit a player score resource
    def put(self, game_name, player_name):
        urlChanged = False

        if not request.json:
            return create_error_response(415, "Unsupported Media Type", "use JSON")
        db_game = Game.query.filter_by(game_token=game_name).first()
        if db_game is None:
            return create_error_response(404, "No game found with name " + str(game_name))
        db_player = Player.query.filter_by(name=player_name).first()
        if db_player is None:
            return create_error_response(404, "No player found with name " + str(player_name))
        db_player_score = PlayerScore.query.filter_by(player=db_player).filter_by(game=db_game).first()
        if db_player_score is None:
            return create_error_response(404, "No score found with player name " + str(player_name)
                + " and game name " + str(game_name))
        try:
            validate(request.json, ScoreBuilder.scoreSchema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))
        
        #If the player of the player score changes
        new_player = request.json["player"]
        if new_player != player_name:
            db_new_player = Player.query.filter_by(name=new_player).first()
            if db_new_player is None:
                return create_error_response(409, "Player does not exist", "No player exists with name "
                    + str(new_player))
            else:
                db_player_score_duplicate = PlayerScore.query.filter_by(game=db_game).filter_by(
                    player=db_new_player).first()
                if db_player_score_duplicate is not None:
                    return create_error_response(409, "Player score already exists", "Player score already "
                       + "exists with name " + str(new_player))
                db_player_score.player = db_new_player
                urlChanged = True
        

        #When score changes
        new_score = request.json["score"]
        db_player_score.score = new_score

        db.session.add(db_player_score)
        db.session.commit()

        #If url changed
        if urlChanged:
            return Response(status=201, headers={
            "Location": url_for("playerscoreresource", player_name=db_player_score.player.name,
                game_name=db_player_score.game.game_token)
            })
        else:
            return Response(status=204)

            


    def delete(self, game_name, player_name):
        db_game = Game.query.filter_by(game_token=game_name).first()
        if db_game is None:
            return create_error_response(404, "No game found with name " + str(game_name))
        db_player = Player.query.filter_by(name=player_name).first()
        if db_player is None:
            return create_error_response(404, "No player found with name " + str(player_name))
        db_player_score = PlayerScore.query.filter_by(player=db_player, game=db_game).first()
        if db_player_score is None:
            return create_error_response(404, "No score found with player name " + str(player_name)
                + " and game name " + str(game_name))
        db.session.delete(db_player_score)
        db.session.commit()

        return Response(status=204)
