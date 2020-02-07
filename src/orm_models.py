#A single game 
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer)
    game_type_id = db.Column(db.Integer, nullable=False, db.ForeignKey("gametype.id", ondelete="SET NULL"))
    host_id = db.Column(db.Integer, nullable=False, db.ForeignKey("player.id", ondelete="SET NULL"))
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournament.id", ondelete="SET NULL")) #Being part of a tournament is optional

    gametype = db.relationship("GameType", back_populates="gametype_game")
    player = db.relationship("Player", back_populates="player_game")
    game_score = db.relationship("PlayerScore", back_populates="score_game")
    tournament = db.relationship("Tournament", back_populates="game")


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(255), nullable=False, unique=True, index=True)
    player_game = db.relationship("Game", back_populates="player")
    player_score = db.relationship("PlayerScore", back_populates="score_player")

class PlayerScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, nullable=False, db.ForeignKey("score_player.id"))
    score = db.Column(db.Float(24))
    game_id = db.Column(db.Integer, nullable=False, db.ForeignKey("score_game.id"))

    score_player = db.relationship("Player", back_populates="player_score")
    score_game = db.relationship("Game", back_populates="game_score")


class GameType(db.Model):


class Leaderboard(db.Model):


class Permission(db.Model):


class Tournament(db.Model):
