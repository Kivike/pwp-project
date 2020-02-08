from app import db, Player, PlayerScore, GameType, Tournament, Game 

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
    chess_game = Game(status=1, game_type=game_type, player=player_1, tournament=tournament)
    chess_game.players.append(player_1)
    chess_game.players.append(player_2)
    chess_game.players.append(player_3)

    #The scores of the players at time point x
    player_1_score = PlayerScore(player=player_1, score=5, game=chess_game)
    player_2_score = PlayerScore(player=player_2, score=10, game=chess_game)
    player_3_score = PlayerScore(player=player_3, score=12, game=chess_game)

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