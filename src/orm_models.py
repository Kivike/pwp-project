from app import db

#A single game 
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer)
    game_type_id = db.Column(db.Integer, db.ForeignKey("game_type.id", ondelete="SET NULL"), nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey("player.id", ondelete="SET NULL"), nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournament.id", ondelete="SET NULL")) #Being part of a tournament is optional

    game_type = db.relationship("GameType", back_populates="gametype_game")
    player = db.relationship("Player", back_populates="player_game")
    game_score = db.relationship("PlayerScore", back_populates="game")
    tournament = db.relationship("Tournament", back_populates="game")


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(255), nullable=False, unique=True, index=True)
    player_game = db.relationship("Game", back_populates="player")
    player_score = db.relationship("PlayerScore", back_populates="player")

class PlayerScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    score = db.Column(db.Float(24))
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)

    player = db.relationship("Player", back_populates="player_score")
    game = db.relationship("Game", back_populates="game_score")


class GameType(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(255), unique=True, nullable=False)
    max_players = db.Column(db.Integer)
    gametype_game = db.relationship("Game", back_populates="game_type")

class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, nullable=False, unique=True, index=True)
    game_type_id = db.Column(db.Integer, nullable=False, unique=True, index=True)
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