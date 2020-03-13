from flask_restful import Resource

class GameScoreboard(Resource):
    def get(self):
        pass #TODO

    def post(self):
        pass #TODO
    
class PlayerScore(Resource):
    def get(self, game_token, player_name):
        pass #TODO

    def put(self, game_token, player_name):
        pass #TODO

    def delete(self, game_token, player_name):
        pass #TODO