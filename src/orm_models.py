class Game(db.Model):



class Player(db.Model):


class PlayerScore(db.Model):


class GameType(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(255), unique=True, nullable=False)
    max_players = db.Column(db.Integer)
    gametype_game = db.relationship("Game", back_populates="gametype")

class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, nullable=False, unique=True, index=True)
    game_id = db.Column(db.Integer, nullable=False, unique=True, index=True)
    wins = db.Column(db.Integer, nullable=False)
    losses = db.Column(db.Integer, nullable=False)

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, nullable=False, index=True)
    key = db.Column(db.String(255), nullable=False) #This is used for permission verification
    value = db.Column(db.String(255))

class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    game = db.relationship("Game", back_populates="tournament")