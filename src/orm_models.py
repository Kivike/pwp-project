from src.extensions import db
from sqlalchemy.sql import func
from flask.cli import with_appcontext
import click



'''This file contains all the ORM models for the database'''

#Represents a single match
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #accessname = db.Column(db.String(255), unique=True, nullable=True)
    status = db.Column(db.Integer, default=0) #1 if active, 0 if not active
    game_type_id = db.Column(db.Integer, db.ForeignKey("game_type.id", ondelete="SET NULL"))
    host_id = db.Column(db.Integer, db.ForeignKey("player.id", ondelete="SET NULL")) #One of the players has to be a host
    tournament_id = db.Column(db.Integer, db.ForeignKey("tournament.id", ondelete="SET NULL")) #Being part of a tournament is optional
    game_token = db.Column(db.String(20), unique=True, nullable=False) 
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    finished_at = db.Column(db.DateTime)

    #Relationships to other models
    game_type = db.relationship("GameType", back_populates="game")
    host = db.relationship("Player", back_populates="game")
    scores = db.relationship("PlayerScore", cascade="all, delete-orphan", back_populates="game")
    tournament = db.relationship("Tournament", back_populates="game")

#Represents a single player, only name defined 
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(255), nullable=False, unique=True, index=True)
    score = db.relationship("PlayerScore", cascade="all, delete-orphan", back_populates="player")
    lboard = db.relationship("Leaderboard", cascade="all, delete-orphan", back_populates="player")
    game = db.relationship("Game", back_populates="host")

#The score of a player in a match
#This also connects players and games to each other
class PlayerScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id", ondelete="CASCADE"), nullable=False)
    score = db.Column(db.Float(24))
    game_id = db.Column(db.Integer, db.ForeignKey("game.id", ondelete="CASCADE"), nullable=False)

    #Relationships to other models
    player = db.relationship("Player", back_populates="score")
    game = db.relationship("Game", back_populates="scores")

    __table__args__ = (db.UniqueConstraint('player_id', 'game_id', '_player_id_game_id_uc'),)

#A type of game, used to differentiate different kind of games from each other 
class GameType(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(255), unique=True, nullable=False)
    max_players = db.Column(db.Integer)
    min_players = db.Column(db.Integer)

    #Relationships to other models
    game = db.relationship("Game", back_populates="game_type")
    lboard = db.relationship("Leaderboard", cascade="all, delete-orphan", back_populates="game_type")

#Used to track how well a player has done in games of different game types
class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id", ondelete="CASCADE"), nullable=False, index=True)
    game_type_id = db.Column(db.Integer, db.ForeignKey("game_type.id", ondelete="CASCADE"), nullable=False, index=True)
    wins = db.Column(db.Integer, nullable=False)
    losses = db.Column(db.Integer, nullable=False)

    #Relationships to other models
    game_type = db.relationship("GameType", back_populates="lboard")
    player = db.relationship("Player", back_populates="lboard")

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


# Initialize database. From:
# https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2020/flask-api-project-layout/#using-the-command-line-interface
@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()