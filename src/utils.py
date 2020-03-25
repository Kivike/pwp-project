import json

from flask import request, Response, url_for



MASON = "application/vnd.mason+json"


class MasonBuilder(dict):
    """
    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.
    """

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.

        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). However we are being lazy and supporting just one
        message.

        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, ns, uri):
        """
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.

        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.

        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md

        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href

class PlayerBuilder(MasonBuilder):
    
    @staticmethod
    def playerSchema():
        schema = {
            "type": "object",
            "required": ["name"]
        }
        props = schema["properties"] = {}
        props["name"] = {
            "description": "Name of the player",
            "type": "string"
        } 
        return schema

    #Controls related to Player and PlayerCollection

    def add_control_all_games(self):
        self.add_control("gamescr:all-games", href=url_for("gamecollection"), title="All games")

    def add_control_all_tournaments(self):
        self.add_control("gamescr:all-tournaments", href=url_for("tournamentcollection"), title="All tournaments")

    def add_control_add_player(self):
        schema = self.playerSchema()
        self.add_control(ctrl_name="gamescr:add-player", href=url_for("playercollection"), 
            method="POST", encoding="json", schema=schema, title="Add a new player")

    def add_control_edit_player(self, name):
        schema = self.playerSchema()
        self.add_control(ctrl_name="edit", href=url_for("playerresource", player_name=name),
            method="PUT", encoding="json", schema=schema, title="Modify the player")
    
    def add_control_delete_player(self, name):
        self.add_control(ctrl_name="gamescr:delete", href=url_for("playerresource", player_name=name), 
            method="DELETE", title="Delete this player")
    
    def add_control_leaderboard(self, name):
        self.add_control(ctrl_name="gamescr:leaderboard", href=url_for("leaderboardplayer", player_name=name), 
            title="Statistics of this player")

class GameBuilder(MasonBuilder):

    @staticmethod
    def gameSchema():
        schema = {
            "type": "object",
            "required": ["name", "game_type", "host"]
        }
        props = schema["properties"] = {}
        props["name"] = {
            "description": "Name used to access the game",
            "type": "string"
        }
        props["status"] = {
            "description": "1 if active, 0 if not active",
            "type": "integer",
            "default": 0
        }
        props["game_type"] = {
            "description": "Name of the game type",
            "type": "string"
        }
        props["host"] = {
            "description": "Name of the player hosting the game",
            "type": "string"
        }
        props["tournament"] = {
            "description": "Name of the tournament the game is a part of",
            "type": "string"
        }
        return schema

    @staticmethod
    def scoreSchema():
        schema = {
            "type": "object",
            "required": ["player", "game", "score"]
        }
        props = schema["properties"] = {}
        props["player"] = {
            "description": "Name of the player",
            "type": "string"
        }
        props["game"] = {
            "description": "Access name of the game",
            "type": "string"
        }
        props["score"] = {
            "description": "Score of the player",
            "type": "float"
        }
        return schema

    # Controls for Game and GameCollection

    def add_control_all_tournaments(self):
        self.add_control("gamescr:all-tournaments", href=url_for("tournamentcollection"), title="All tournaments")

    def add_control_all_gametypes(self):
        self.add_control("gamescr:all-gametypes", href=url_for("gametypecollection"), title="All gametypes")

    def add_control_all_players(self):
        self.add_control("gamescr:all-players", href=url_for("playercollection"), title="All players")

    def add_control_add_game(self):
        schema = self.gameSchema()
        self.add_control(ctrl_name="gamescr:add-game", href=url_for("gamecollection"), method="POST", 
            encoding="json", schema=schema, title="Add a new game")

    def add_control_gametype(self, name):
        self.add_control(ctrl_name="gamescr:gametype", href=url_for("gametyperesource", gametype_name=name), 
            title="Gametype of this game")

    def add_control_scores(self, name):
        self.add_control(ctrl_name="gamescr:scores", href=url_for("gamescoreboard", game_token=name), 
            title="Scores of players in this game")

    def add_control_tournament(self, name):
        self.add_control(ctrl_name="gamescr:tournament", href=url_for("tournamentresource", tournament_token=name), 
            title="Tournament associated with this game")

    def add_control_add_score(self, name):
        schema = self.scoreSchema()
        self.add_control(ctrl_name="gamescr:add-score", href=url_for("gamescoreboard", game_token=name), 
            method="POST", encoding="json", schema=schema, title="Add a new player to the game")

    def add_control_edit_game(self, name):
        schema = self.gameSchema()
        self.add_control(ctrl_name="edit", href=url_for("gameresource", game_token=name), method="PUT", 
            encoding="json", schema=schema, title="Edit this game")

    def add_control_delete_game(self, name):
        self.add_control(ctrl_name="gamescr:delete", href=url_for("gameresource", game_token=name), 
            method="DELETE", title="Delete this game")

class GametypeBuilder(MasonBuilder):

    @staticmethod
    def gametypeSchema():
        schema = {
            "type": "object",
            "required": ["name"]
        }
        props = schema["properties"] = {}
        props["name"] = {
            "description": "Name of the game type",
            "type": "string"
        }
        props["max_players"] = {
            "description": "Maximum amount of players allowed per game",
            "type": "integer"
        }
        props["min_players"] = {
            "description": "Minimum amount of players per game",
            "type": "integer"
        }
        return schema

    #Controls for Gametype Collection and Resource

    def add_control_all_games(self):
        self.add_control("gamescr:all-games", href=url_for("gamecollection"), title="All games")

    def add_control_add_gametype(self):
        schema = self.gametypeSchema()
        self.add_control(ctrl_name="gamescr:add-gametype", href=url_for("gametypecollection"), method="POST", 
            encoding="json", schema=schema, title="Add a new gametype")

    def add_control_edit_gametype(self, name):
        schema = self.gametypeSchema()
        self.add_control(ctrl_name="edit", href=url_for("gametyperesource", gametype_name=name), method="PUT", 
            encoding="json", schema=schema, title="Edit this gametype")

    def add_control_leaderboard(self, name):
        self.add_control(ctrl_name="gamescr:leaderboard", href=url_for("leaderboardgametype", gametype_name=name), 
            title="Leaderboard for this gametype")

    def add_control_delete_gametype(self, name):
        self.add_control(ctrl_name="gamescr:delete", href=url_for("gametyperesource", gametype_name=name), 
            method="DELETE", title="Delete this gametype")

class ScoreBuilder(MasonBuilder):
    
    @staticmethod
    def scoreSchema():
        schema = {
            "type": "object",
            "required": ["player", "game", "score"]
        }
        props = schema["properties"] = {}
        props["player"] = {
            "description": "Name of the player",
            "type": "string"
        }
        props["game"] = {
            "description": "Access name of the game",
            "type": "string"
        }
        props["score"] = {
            "description": "Score of the player",
            "type": "float"
        }
        return schema

    #Controls for GameScoreboard and PlayerScoreResources

    def add_control_add_score(self, name):
        schema = self.scoreSchema()
        self.add_control(ctrl_name="gamescr:add-score", href=url_for("gamescoreboard", game_token=name), 
            method="POST", encoding="json", schema=schema, title="Add a new player to the game")

    def add_control_edit_playerscore(self, game_token, player_name):
        schema = self.scoreSchema()
        self.add_control(ctrl_name="edit", href=url_for("playerscoreresource", game_token=game_token, 
            player_name=player_name), method="PUT", encoding="json", schema=schema, title="Edit player's score")

    def add_control_delete_gametype(self, game_token, player_name):
        self.add_control(ctrl_name="gamescr:delete", href=url_for("playerscoreresource", game_token=game_token, 
            player_name=player_name), method="DELETE", title="Delete this player from this game")

    def add_control_player(self, player_name):
        self.add_control(ctrl_name="gamescr:player", href=url_for("playerresource", player_name=player_name), 
            title="Access the player of this score")


def create_error_response(status_code, title, message=None):
    resource_url = request.path
    body = MasonBuilder(resource_url=resource_url)
    body.add_error(title, message)
    body.add_control("profile", href="/profiles/error/")
    return Response(json.dumps(body), status_code, mimetype=MASON)