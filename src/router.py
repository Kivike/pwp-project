from src.resource.game import GameResource, GameCollection
from src.resource.gametype import GametypeResource, GametypeCollection
from src.resource.leaderboard import LeaderboardGametype, LeaderboardPlayer
from src.resource.player import PlayerResource, PlayerCollection
from src.resource.score import GameScoreboard, PlayerScoreResource
from src.resource.tournament import TournamentResource, TournamentCollection
from src.utils import MasonBuilder
import json

from flask_restful import Api, url_for
from flask import Response

MASON = "application/vnd.mason+json"
NAMESPACE_URL = "/gamescore/link-relations#"

def route_app(app):
    api = Api(app)

    @app.route("/")
    def index():
        return app.send_static_file("html/index.html")

    @app.route("/api/")
    def entry():
        body = MasonBuilder()
        body.add_namespace("gamescr", NAMESPACE_URL)
        body.add_control("gamescr:all-tournaments", href=url_for("tournamentcollection"), title="All tournaments")
        body.add_control("gamescr:all-games", href=url_for("gamecollection"), title="All games")
        body.add_control("gamescr:all-players", href=url_for("playercollection"), title="All players")
        return Response(json.dumps(body), 200, mimetype=MASON)

    api.add_resource(GameResource, "/api/games/<game_name>/")
    api.add_resource(GameCollection, "/api/games/")

    api.add_resource(GametypeResource, "/api/gametypes/<gametype_name>/")
    api.add_resource(GametypeCollection, "/api/gametypes/")

    api.add_resource(PlayerResource, "/api/players/<player_name>/")
    api.add_resource(PlayerCollection, "/api/players/")

    api.add_resource(GameScoreboard, "/api/games/<game_name>/scoreboard/")
    api.add_resource(PlayerScoreResource, "/api/games/<game_name>/scoreboard/<player_name>/")

    route_leaderboard(app, api)
    route_tournament(app, api)

def route_leaderboard(app, api): # pragma: no cover
    '''
    Not yet implemented
    '''
    api.add_resource(
        LeaderboardGametype,
        "/api/leaderboard/gametype/<gametype_name>/",
        "/api/gametype/<gametype_name>/leaderboard/"
    )
    api.add_resource(
        LeaderboardPlayer,
        "/api/leaderboard/player/<player_name>/",
        "/api/players/<player_name>/leaderboard/"
    )

def route_tournament(app, api): # pragma: no cover
    '''
    Not yet implemented
    '''
    api.add_resource(TournamentResource, "/api/tournaments/<tournament_token>/")
    api.add_resource(TournamentCollection, "/api/tournaments/")