from src.app import db
from sqlalchemy.sql import func

'''This file contains all the ORM models for the database'''

#Represents a single match
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, default=0) #1 if active, 0 if not active
    game_type_id = db.Column(db.Integer, db.ForeignKey("game_type.id", ondelete="SET NULL"))
    host_id = db.Column(db.Integer, db.ForeignKey("player.id", ondelete="SET NULL")) #One of the players has to be a host
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournament.id", ondelete="SET NULL")) #Being part of a tournament is optional
    game_token = db.Column(db.String(20), nullable=False) 
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    finished_at = db.Column(db.DateTime)

    #Relationships to other models
    game_type = db.relationship("GameType", back_populates="game")
    host = db.relationship("Player")
    scores = db.relationship("PlayerScore", back_populates="game")
    tournament = db.relationship("Tournament", back_populates="game")

#Represents a single player, only name defined 
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(255), nullable=False, unique=True, index=True)

#The score of a player in a match
#This also connects players and games to each other
class PlayerScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    score = db.Column(db.Float(24))
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)

    #Relationships to other models
    player = db.relationship("Player")
    game = db.relationship("Game", back_populates="scores")

#A type of game, used to differentiate different kind of games from each other 
class GameType(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(255), unique=True, nullable=False)
    max_players = db.Column(db.Integer)
    min_players = db.Column(db.Integer)

    #Relationships to other models
    game = db.relationship("Game", back_populates="game_type")

#Used to track how well a player has done in games of different game types
class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id", ondelete="CASCADE"), nullable=False, index=True)
    game_type_id = db.Column(db.Integer, db.ForeignKey("game_type.id", ondelete="CASCADE"), nullable=False, index=True)
    wins = db.Column(db.Integer, nullable=False)
    losses = db.Column(db.Integer, nullable=False)

    #Relationships to other models
    game_type = db.relationship("GameType")
    player = db.relationship("Player")

    #every player_id and game_type_id combination is unique
    __table__args__ = (db.UniqueConstraint('player_id', 'game_type_id', '_player_id_game_type_id_uc'),)

#Optional, can be used for different tournaments
class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    status = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    finished_at = db.Column(db.DateTime)

    game = db.relationship("Game", back_populates="tournament")