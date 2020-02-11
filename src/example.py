from app import db, create_app
from orm_models import Player, PlayerScore, GameType, Tournament, Game 

app = create_app('dev')
app_context = app.app_context()
app_context.push()

db.drop_all()   

db.create_all()



#This script creates an example data base
def populate_db():

    #Players
    player_1 = Player(name="Alice")
    player_2 = Player(name="Bob")
    player_3 = Player(name="Charles")

    #Example game type
    game_type = GameType(name="chess", max_players=3)

    #Create a chess tournament
    tournament = Tournament(name="Chess Tournament 1")

    #Initialize a game and add the players
    chess_game = Game(status=1, game_type=game_type, host=player_1, tournament=tournament)

    #Initial player scores
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

populate_db()