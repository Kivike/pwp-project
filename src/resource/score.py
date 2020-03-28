from flask_restful import Resource

class GameScoreboard(Resource):
    def get(self, game_name):
        pass #TODO

    def post(self, game_name):
        pass #TODO
    
class PlayerScoreResource(Resource):
    def get(self, game_name, player_name):
        pass #TODO

    def put(self, game_name, player_name):
        pass #TODO

    def delete(self, game_name, player_name):
        pass #TODO