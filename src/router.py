from src.resource.game import Game, GameCollection
from src.resource.gametype import Gametype, GametypeCollection
from src.resource.leaderboard import LeaderboardGametype, LeaderboardPlayer
from src.resource.player import Player, PlayerCollection
from src.resource.score import GameScoreboard, PlayerScore
from src.resource.tournament import Tournament, TournamentCollection

from flask_restful import Api

def route_app(app):
    api = Api(app)

    @app.route("/")
    def index():
        return "Index"

    api.add_resource(Game, "/api/games/<game_token>/")
    api.add_resource(GameCollection, "/api/games/")

    api.add_resource(Gametype, "/api/gametypes/<gametype_name>/")
    api.add_resource(GametypeCollection, "/api/gametypes/")

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

    api.add_resource(Player, "/api/players/<player_name>/")
    api.add_resource(PlayerCollection, "/api/players/")

    api.add_resource(GameScoreboard, "/api/games/<game_token>/scoreboard/")
    api.add_resource(PlayerScore, "/api/games/<game_token>/scoreboard/<player_name>/")

    api.add_resource(Tournament, "/api/tournaments/<tournament_token>/")
    api.add_resource(TournamentCollection, "/api/tournaments/")