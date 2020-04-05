from src.app import db, create_app
from src.orm_models import Player, PlayerScore, GameType, Tournament, Game, Leaderboard 
from sqlalchemy.sql import func
import datetime

'''This is used to create an example populated database. Can be run from 
the root folder of the project with 'python -m src.example' '''

#Setup the database
app = create_app('development')
app_context = app.app_context()
app_context.push()

db.drop_all()   

db.create_all()

#This function creates example data in the database
def first_example():

    #GAME 1 - A chess game with 3 players

    #Players
    player_1 = Player(name="Alice")
    player_2 = Player(name="Bob")
    player_3 = Player(name="Charles")

    #Example game type
    game_type = GameType(name="chess", max_players=3)

    #Create a chess tournament (created_at defaults to func.now() but is here as an example)
    tournament = Tournament(name="Chess Tournament 1", status=1, created_at=func.now())

    #Initialize a game and add the players (created_at defaults to func.now() but is here as an example)
    chess_game = Game(game_token="testgame1" ,status=1, game_type=game_type, host=player_1, tournament=tournament, created_at=func.now())

    #Initial player scores, the points are optional
    player_1_score = PlayerScore(player=player_1, game=chess_game)
    player_2_score = PlayerScore(player=player_2, game=chess_game)
    player_3_score = PlayerScore(player=player_3, game=chess_game)

    #Connect the player scores to the game
    chess_game.scores.append(player_1_score)
    chess_game.scores.append(player_2_score)
    chess_game.scores.append(player_3_score)

    #Add the created things to the database
    db.session.add(player_1)
    db.session.add(player_2)
    db.session.add(player_3)

    db.session.add(game_type)
    db.session.add(tournament)
    db.session.add(chess_game)
    db.session.add(player_1_score)
    db.session.add(player_2_score)
    db.session.add(player_3_score)

    db.session.commit()

#This function creates more example data in the database
def second_example():
    
    #GAME 2 - Hearts game with 4 players

    #players 
    player_1 = Player(name="Jessica")
    player_2 = Player(name="Ken")
    player_3 = Player(name="Laura")
    player_4 = Player(name="Maurice")

    #game type
    game_type = GameType(name="Hearts", max_players=4)

    #No tournament this time as it is optional

    #Initialize a game and add the players, in this example game has already ended
    hearts_game = Game(game_token="gameofhearts", status=0, game_type=game_type, host=player_1, created_at=datetime.datetime.now()-datetime.timedelta(days=5), finished_at=datetime.datetime.now()-datetime.timedelta(days=2))

    #Player scores, this time they have scores
    player_1_score = PlayerScore(player=player_1, score=22, game=hearts_game)
    player_2_score = PlayerScore(player=player_2, score=35, game=hearts_game)
    player_3_score = PlayerScore(player=player_3, score=102, game=hearts_game)
    player_4_score = PlayerScore(player=player_4, score=24, game=hearts_game)

    #Connect the players scores to the game
    hearts_game.scores.append(player_1_score)
    hearts_game.scores.append(player_2_score)
    hearts_game.scores.append(player_3_score)
    hearts_game.scores.append(player_4_score)

    #Add the created things to database
    db.session.add(player_1)
    db.session.add(player_2)
    db.session.add(player_3)

    db.session.add(game_type)
    db.session.add(hearts_game)
    db.session.add(player_1_score)
    db.session.add(player_2_score)
    db.session.add(player_3_score)

    db.session.commit()

    #Let's create a leaderboard

    player_1_leaderboard = Leaderboard(player_id=player_1.id, game_type_id=hearts_game.id, wins=5, losses=3)
    player_2_leaderboard = Leaderboard(player_id=player_2.id, game_type_id=hearts_game.id, wins=4, losses=6)
    player_3_leaderboard = Leaderboard(player_id=player_3.id, game_type_id=hearts_game.id, wins=2, losses=5)
    player_4_leaderboard = Leaderboard(player_id=player_4.id, game_type_id=hearts_game.id, wins=0, losses=3)

    #Add the leaderboard entries to the db
    db.session.add(player_1_leaderboard)
    db.session.add(player_2_leaderboard)
    db.session.add(player_3_leaderboard)
    db.session.add(player_4_leaderboard)
    db.session.commit()

first_example()

second_example()