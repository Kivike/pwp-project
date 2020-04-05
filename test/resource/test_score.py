import unittest
from sqlalchemy import exc
from sqlalchemy import orm

from src.app import create_app, db
from src.orm_models import Player, Game, PlayerScore, GameType

import json

SCORE_URL = "/api/games/<game_token>/scoreboard/<player_name>/"
SCOREBOARD_URL = "/api/games/<game_token>/scoreboard/"
GAME_URL = "/api/games/<game_token>/"
PLAYER_URL = "/api/players/<player_name>/"

class TestScore(unittest.TestCase):

    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def testGetNonExistingGameScoreboard(self):
        url = SCOREBOARD_URL.replace("<game_token>", "doesnotexist123")
        response = self.client.get(url)
        
        assert response.status_code == 404, response.status_code

    def testGetGameEmptyScoreboard(self):
        game_type = GameType(name="Uno")
        game = Game(game_token="test12345", game_type=game_type)

        db.session.add(game_type)
        db.session.add(game)
        db.session.commit()

        url = SCOREBOARD_URL.replace("<game_token>", "test12345")
        response = self.client.get(url)
        
        assert response.status_code == 200

        data = json.loads(response.data.decode("utf-8"))
        assert len(data["items"]) == 0

    def testGetGameScoreboard(self):
        game_type = GameType(name="Uno")
        game = Game(game_token="test12345", game_type=game_type)
        player_a = Player(name="Testman A")
        player_b = Player(name="Testman B")
        score_a = PlayerScore(player=player_a, game=game, score=8.5)
        score_b = PlayerScore(player=player_b, game=game)

        db.session.add(game_type)
        db.session.add(game)
        db.session.add(player_a)
        db.session.add(player_b)
        db.session.add(score_a)
        db.session.add(score_b)
        db.session.commit()

        url = SCOREBOARD_URL.replace("<game_token>", "test12345")
        response = self.client.get(url)
        
        assert response.status_code == 200

        data = json.loads(response.data.decode("utf-8"))
        assert len(data["items"]) == 2

    def testPostValidScore(self):
        game = Game(game_token="test12345")
        player = Player(name="Jamppa")

        db.session.add(game)
        db.session.add(player)
        db.session.commit()

        url = SCOREBOARD_URL.replace("<game_token>", "test12345")

        post_data = {
            "player": "Jamppa",
            "score": 5
        }

        response = self.client.post(
            url,
            data=json.dumps(post_data),
            content_type="application/json"
        )

        assert response.status_code == 201, response.status_code
        assert PlayerScore.query.filter_by(player_id=1).count() == 1

    def testPostScoreWithoutPlayer(self):
        game_type = GameType(name="Uno")
        game = Game(game_token="test12345", game_type=game_type)

        db.session.add(game)
        db.session.commit()

        url = SCOREBOARD_URL.replace("<game_token>", "test12345")

        post_data = {"foo": 1}

        response = self.client.post(
            url,
            data=json.dumps(post_data),
            content_type="application/json"
        )

        assert response.status_code == 400, response.status_code

    def testPostScoreNonExistingGame(self):
        player = Player(name="Jamppa")

        db.session.add(player)
        db.session.commit()

        url = SCOREBOARD_URL.replace("<game_token>", "nonexisting")

        post_data = {
            "player": "Jamppa",
            "score": 5
        }

        response = self.client.post(
            url,
            data=json.dumps(post_data),
            content_type="application/json"
        )

        assert response.status_code == 404, response.status_code

    def testGetPlayerScore(self):
        game_type = GameType(name="Uno")
        game = Game(game_token="test12345", game_type=game_type)
        player = Player(name="Jamppa")
        score = PlayerScore(game=game, player=player)

        db.session.add(game_type)
        db.session.add(game)
        db.session.add(player)
        db.session.add(score)
        db.session.commit()

        url = SCORE_URL.replace("<game_token>", "test12345")
        url = url.replace("<player_name>", "Jamppa")

        response = self.client.get(url)
        assert response.status_code == 200, response.status_code

    def testGetNonExistingGamePlayerScore(self):
        """
        Error test for retrieving player score for nonexisting game
        """
        player = Player(name="Jamppa")
        db.session.add(player)
        db.session.commit()

        url = SCORE_URL.replace("<game_token>", "nothere")
        url = url.replace("<player_name>", "Jamppa")
        response = self.client.get(url)

        assert response.status_code == 404, response.status_code

    def testGetNonExistingPlayerPlayerScore(self):
        """
        Error test for retrieving player score for nonexisting player
        """
        game_type = GameType(name="Uno")
        game = Game(game_token="test12345", game_type=game_type)
        db.session.add(game_type)
        db.session.add(game)
        db.session.commit()

        url = SCORE_URL.replace("<game_token>", "test12345")
        url = url.replace("<player_name>", "idontexist")
        response = self.client.get(url)

        assert response.status_code == 404, response.status_code

    def testGetNonExistingPlayerScore(self):
        """
        Error test when player and game exist, but the player score does not
        """
        game_type = GameType(name="Uno")
        game = Game(game_token="test12345", game_type=game_type)
        player = Player(name="Jamppa")

        db.session.add(game_type)
        db.session.add(game)
        db.session.add(player)
        db.session.commit()

        url = SCORE_URL.replace("<game_token>", "test12345")
        url = url.replace("<player_name>", "Jamppa")
        response = self.client.get(url)

        assert response.status_code == 404, response.status_code

    def testPutScoreEditScore(self):
        """
        Make a valid put request to change score value of a PlayerScore
        """
        game_type = GameType(name="Uno")
        game = Game(game_token="test12345", game_type=game_type)
        player = Player(name="Jamppa")
        score = PlayerScore(game=game, player=player)

        db.session.add(game_type)
        db.session.add(game)
        db.session.add(player)
        db.session.add(score)
        db.session.commit()

        put_data = {
            "player": "Jamppa",
            "score": 50
        }

        url = SCORE_URL.replace("<game_token>", "test12345")
        url = url.replace("<player_name>", "Jamppa")

        response = self.client.put(
            url,
            data=json.dumps(put_data),
            content_type="application/json"
        )

        assert response.status_code == 204, response.status_code

        db_score = PlayerScore.query.filter_by(player_id=player.id).first()
        assert db_score.score == 50, db_score.score

    def testPutScoreNonExistingGame(self):
        player = Player(name="Jamppa")
        db.session.add(player)
        db.session.commit()

        put_data = {
            "player": "Jamppa",
            "score": 50
        }
        url = SCORE_URL.replace("<game_token>", "10dchess123")
        url = url.replace("<player_name>", "Jamppa")

        response = self.client.put(
            url,
            data=json.dumps(put_data),
            content_type="application/json"
        )

        assert response.status_code == 404, response.status_code

    def testPutScoreNonExistingPlayer(self):
        game_type = GameType(name="Uno")
        game = Game(game_token="test12345", game_type=game_type)

        db.session.add(game_type)
        db.session.add(game)
        db.session.commit()

        url = SCORE_URL.replace("<game_token>", "test12345")
        url = url.replace("<player_name>", "Jamppa")

        put_data = {
            "player": "Jamppa",
            "score": 10
        }

        response = self.client.put(
            url,
            data=json.dumps(put_data),
            content_type="application/json"
        )

        assert response.status_code == 404, response.status_code

    def testPutScoreNonExistingScore(self):
        game_type = GameType(name="Uno")
        game = Game(game_token="test12345", game_type=game_type)
        player = Player(name="Jamppa")

        db.session.add(game_type)
        db.session.add(game)
        db.session.add(player)
        db.session.commit()

        url = SCORE_URL.replace("<game_token>", "test12345")
        url = url.replace("<player_name>", "Jamppa")

        put_data = {
            "player": "Jamppa",
            "score": 10
        }

        response = self.client.put(
            url,
            data=json.dumps(put_data),
            content_type="application/json"
        )

        assert response.status_code == 404, response.status_code

    def testPutScoreDuplicatePlayer(self):
        """
        Change player of a score to one that already has score for the game
        """
        game_type = GameType(name="Uno")
        game = Game(game_token="test12345", game_type=game_type)
        player_a = Player(name="Player A")
        player_b = Player(name="Player B")
        score_a = PlayerScore(game=game, player=player_a)
        score_b = PlayerScore(game=game, player=player_b)

        db.session.add(game_type)
        db.session.add(game)
        db.session.add(player_a)
        db.session.add(player_b)
        db.session.add(score_a)
        db.session.add(score_b)
        db.session.commit()

        put_data = {
            "player": "Player B",
            "score": 100,
            "game": "test12345"
        }
        url = SCORE_URL.replace("<game_token>", "test12345")
        url = url.replace("<player_name>", "Player A")

        response = self.client.put(
            url,
            data=json.dumps(put_data),
            content_type="application/json"
        )
        assert response.status_code == 409, response.status_code

    def testPutScoreInvalidSchema(self):
        game_type = GameType(name="Uno")
        game = Game(game_token="test12345", game_type=game_type)
        player = Player(name="Jamppa")
        score = PlayerScore(game=game, player=player)

        db.session.add(game_type)
        db.session.add(game)
        db.session.add(player)
        db.session.add(score)
        db.session.commit()

        put_data = {
            "color": "green"
        }

        url = SCORE_URL.replace("<game_token>", "test12345")
        url = url.replace("<player_name>", "Jamppa")

        response = self.client.put(
            url,
            data=json.dumps(put_data),
            content_type="application/json"
        )

        assert response.status_code == 400, response.status_code

    def testPutScoreMissingContentType(self):
        game_type = GameType(name="Uno")
        game = Game(game_token="test12345", game_type=game_type)
        player = Player(name="Jamppa")
        score = PlayerScore(game=game, player=player)

        db.session.add(game_type)
        db.session.add(game)
        db.session.add(player)
        db.session.add(score)
        db.session.commit()

        put_data = {
            "player": "Jamppa",
            "score": 50
        }

        url = SCORE_URL.replace("<game_token>", "test12345")
        url = url.replace("<player_name>", "Jamppa")

        response = self.client.put(
            url,
            data=json.dumps(put_data)
        )

        assert response.status_code == 415, response.status_code

    def testDeleteExistingPlayerScore(self):
        game_type = GameType(name="Uno")
        game = Game(game_token="test12345", game_type=game_type)
        player = Player(name="Jamppa")
        score = PlayerScore(game=game, player=player)

        db.session.add(game_type)
        db.session.add(game)
        db.session.add(player)
        db.session.add(score)

        url = SCORE_URL.replace("<game_token>", "test12345")
        url = url.replace("<player_name>", "Jamppa")
        response = self.client.delete(url)

        assert response.status_code == 204, response.status_code

    def testDeleteScoreNonExistingGame(self):
        player = Player(name="Jamppa")
        db.session.add(player)
        db.session.commit()

        url = SCORE_URL.replace("<game_token>", "test12345")
        url = url.replace("<player_name>", "Jamppa")
        response = self.client.delete(url)

        assert response.status_code == 404, response.status_code

    def testDeleteScoreNonExistingPlayer(self):
        game_type = GameType(name="Uno")
        game = Game(game_token="test12345", game_type=game_type)
        
        db.session.add(game_type)
        db.session.add(game)
        db.session.commit()

        url = SCORE_URL.replace("<game_token>", "test12345")
        url = url.replace("<player_name>", "idontexist")

        response = self.client.delete(url)

        assert response.status_code == 404, response.status_code

    def testDeleteNonExistingScore(self):
        game_type = GameType(name="Uno")
        game = Game(game_token="test12345", game_type=game_type)
        player = Player(name="Jamppa")

        db.session.add(game_type)
        db.session.add(game)
        db.session.add(player)

        url = SCORE_URL.replace("<game_token>", "test12345")
        url = url.replace("<player_name>", "Jamppa")
        response = self.client.delete(url)

        assert response.status_code == 404, response.status_code

    def testDeleteGameDeletesScores(self):
        """
        Test that deleting game of a score also deletes scores for that game
        """
        game_type = GameType(name="Uno")
        game = Game(game_token="test12345", game_type=game_type)
        player_a = Player(name="Testman A")
        player_b = Player(name="Testman B")
        score_a = PlayerScore(player=player_a, game=game)
        score_b = PlayerScore(player=player_b, game=game)

        db.session.add(game_type)
        db.session.add(game)
        db.session.add(player_a)
        db.session.add(player_b)
        db.session.add(score_a)
        db.session.add(score_b)
        db.session.commit()

        url = GAME_URL.replace("<game_token>", "test12345")
        response = self.client.delete(url)
        
        assert response.status_code == 204
        assert PlayerScore.query.count() == 0, PlayerScore.query.count()

    def testDeleteScorePlayerDeletesScore(self):
        """Test that deleting player of a score also deletes the score of that player"""
        game_type = GameType(name="Uno")
        game = Game(game_token="test12345", game_type=game_type)
        player = Player(name="Testman")
        score = PlayerScore(player=player, game=game)

        db.session.add(game_type)
        db.session.add(game)
        db.session.add(player)
        db.session.add(score)

        player_url = PLAYER_URL.replace("<player_name>", "Testman")
        self.client.delete(player_url)

        assert PlayerScore.query.count() == 0, PlayerScore.query.count()

