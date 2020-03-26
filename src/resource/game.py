from flask_restful import Resource, url_for
from flask import request, Response
from sqlalchemy.exc import IntegrityError
from src.utils import GameBuilder
from src.utils import create_error_response
from src.orm_models import Game
from src.extensions import db
import json
from jsonschema import validate, ValidationError

MASON = "application/vnd.mason+json"
NAMESPACE_URL = "/gamescore/link-relations#"
PROFILE_URL = "/profiles/game/"

class GameCollection(Resource):
    def get(self):
        pass #TODO

    def post(self):
        pass #TODO

class GameResource(Resource):
    def get(self, game_name):
        pass #TODO

    def put(self, game_name):
        pass #TODO

    def delete(self, game_name):
        pass #TODO
