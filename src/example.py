from src.app import db, create_app
from src.orm_models import Player, PlayerScore, GameType, Tournament, Game, Leaderboard 

app = create_app('dev')
app_context = app.app_context()
app_context.push()

db.drop_all()   

db.create_all()



#This script creates example data in the database
def first_example():

    #GAME 1 - A chess game with 3 players

    #Players
    player_1 = Player(name="Alice")
    player_2 = Player(name="Bob")
    player_3 = Player(name="Charles")

    #Example game type
    game_type = GameType(name="chess", max_players=3)

    #Create a chess tournament
    tournament = Tournament(name="Chess Tournament 1")

    #Initialize a game and add the players
    chess_game = Game(status=1, game_type=game_type, host=player_1, tournament=tournament, game_token="chess_token")

    #Initial player scores, the points are optional
    player_1_score = PlayerScore(player=player_1, game=chess_game)
    player_2_score = PlayerScore(player=player_2, game=chess_game)
    player_3_score = PlayerScore(player=player_3, game=chess_game)

    chess_game.scores.append(player_1_score)
    chess_game.scores.append(player_2_score)
    chess_game.scores.append(player_3_score)

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


#This script creates more example data in the database
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

    #Initialize a game and add the players
    hearts_game = Game(status=1, game_type=game_type, host=player_1, game_token="hearts_token")

    #Player scores, this time they have scores
    player_1_score = PlayerScore(player=player_1, score=22, game=hearts_game)
    player_2_score = PlayerScore(player=player_2, score=35, game=hearts_game)
    player_3_score = PlayerScore(player=player_3, score=95, game=hearts_game)
    player_4_score = PlayerScore(player=player_4, score=24, game=hearts_game)

    hearts_game.scores.append(player_1_score)
    hearts_game.scores.append(player_2_score)
    hearts_game.scores.append(player_3_score)
    hearts_game.scores.append(player_4_score)

    hearts_game.scores.append(player_1_score)
    hearts_game.scores.append(player_2_score)
    hearts_game.scores.append(player_3_score)

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


    db.session.add(player_1_leaderboard)
    db.session.add(player_2_leaderboard)
    db.session.add(player_3_leaderboard)
    db.session.add(player_4_leaderboard)
    db.session.commit()




first_example()

second_example()